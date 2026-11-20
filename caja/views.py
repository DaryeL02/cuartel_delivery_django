from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.db import IntegrityError, transaction
from rest_framework.authtoken.models import Token

from core.models import Caja, MovimientoCaja
from core.permissions import RoleBasedIsAuthenticated
from .serializers import CajaSerializer, MovimientoManualSerializer, MovimientoSerializer


class PuedeAbrirCaja(RoleBasedIsAuthenticated):
    message = 'No tiene los permisos adecuados para abrir una caja'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.method != 'POST':
            return True
        return request.user.usuarios_roles.filter(
            Q(rol__nombre__iexact='Dueño')
            | Q(rol__nombre__iexact='Dueno')
            | Q(rol__nombre__iexact='Administrador')
        ).exists()


class CajasAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PuedeAbrirCaja]

    def get(self, request):
        cajas = Caja.objects.all().select_related(
            'usuario__empleado'
        ).prefetch_related(
            'movimientos'
        )

        status_param = request.query_params.get('status', None)
        date_param = request.query_params.get('date', None)
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')

        hoy = timezone.localdate()
        condicion_activa = Q(estado=True) | Q(fecha_hora_cierre__isnull=True)
        condicion_hoy = Q(fecha_hora_apertura__date=hoy) | Q(fecha_hora_cierre__date=hoy)

        if fecha_desde:
            cajas = cajas.filter(fecha_hora_apertura__date__gte=fecha_desde)
        if fecha_hasta:
            cajas = cajas.filter(fecha_hora_apertura__date__lte=fecha_hasta)

        if status_param == 'active' and date_param == 'today':
            cajas = cajas.filter(condicion_hoy | condicion_activa)
        elif status_param == 'active':
            cajas = cajas.filter(condicion_activa)
        elif date_param == 'today':
            cajas = cajas.filter(condicion_hoy | condicion_activa)

        cajas = cajas.order_by('-estado', '-fecha_hora_apertura')

        serializer = CajaSerializer(cajas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        password = request.data.get('password')
        if not isinstance(password, str) or not password:
            return Response(
                {'password': 'Debes ingresar tu contraseña para abrir la caja.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.user.check_password(password):
            return Response(
                {'password': 'La contraseña ingresada es incorrecta.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        datos = request.data.copy()
        datos.pop('password', None)
        datos['usuario'] = request.user.id_usuarios
        serializer = CajaSerializer(data=datos, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        local_id = serializer.validated_data['local'].id_locales
        caja_abierta = Caja.objects.filter(
            local_id=local_id,
        ).filter(Q(estado=True) | Q(fecha_hora_cierre__isnull=True)).exists()

        if caja_abierta:
            return Response(
                {"detail": "Ya existe una caja abierta en el local."},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            serializer.save()
        except IntegrityError:
            return Response(
                {"detail": "Ya existe una caja abierta en el local."},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CajasDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [RoleBasedIsAuthenticated]

    def get(self, request, pk):
        caja = get_object_or_404(Caja, pk=pk)
        serializer = CajaSerializer(caja, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def patch(self, request, pk):
        caja = get_object_or_404(Caja.objects.select_for_update(), pk=pk)

        if caja.usuario_id != request.user.id_usuarios:
            return Response(
                {"detail": "Solo puedes cerrar una caja asignada a tu usuario."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not caja.estado and caja.fecha_hora_cierre is not None:
            return Response(
                {"detail": "Esta caja ya está cerrada."},
                status=status.HTTP_409_CONFLICT,
            )

        if request.data.get('confirmar_cierre') is not True:
            return Response(
                {"detail": "Debes confirmar explícitamente el cierre de caja."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CajaSerializer(
            caja, data=request.data, partial=True, context={'request': request}
        )

        if serializer.is_valid():
            caja = serializer.save()
            return Response(CajaSerializer(caja, context={'request': request}).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [RoleBasedIsAuthenticated]
    acceso_operativo_pedidos = True
    metodos_operativos_permitidos = {'POST'}

    def post(self, request):
        caja_abierta = Caja.objects.filter(
            usuario=request.user,
        ).filter(Q(estado=True) | Q(fecha_hora_cierre__isnull=True)).exists()

        if caja_abierta:
            return Response(
                {"detail": "No puedes cerrar sesión mientras tengas una caja abierta."},
                status=status.HTTP_409_CONFLICT,
            )

        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_200_OK)


class MovimientosCajaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [RoleBasedIsAuthenticated]

    def get(self, request):
        movimientos = MovimientoCaja.objects.select_related(
            'caja__usuario', 'venta', 'compra'
        ).order_by('-fecha_hora_creacion')
        caja_id = request.query_params.get('caja')
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')
        if caja_id:
            movimientos = movimientos.filter(caja_id=caja_id)
        if desde:
            movimientos = movimientos.filter(fecha_hora_creacion__date__gte=desde)
        if hasta:
            movimientos = movimientos.filter(fecha_hora_creacion__date__lte=hasta)
        return Response(MovimientoSerializer(movimientos, many=True).data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        serializer = MovimientoManualSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        caja = get_object_or_404(
            Caja.objects.select_for_update(),
            pk=serializer.validated_data['caja'].pk,
        )
        if caja.usuario_id != request.user.id_usuarios:
            return Response(
                {'detail': 'Solo puedes registrar movimientos en una caja asignada a tu usuario.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not caja.estado or caja.fecha_hora_cierre is not None:
            return Response(
                {'detail': 'Solo puedes registrar movimientos en una caja abierta.'},
                status=status.HTTP_409_CONFLICT,
            )

        movimiento_data = serializer.validated_data
        monto = movimiento_data['monto']
        if (
            movimiento_data['tipo_movimiento'] == MovimientoCaja.TipoMovimiento.EGRESO
            and monto > caja.saldo_actual
        ):
            return Response(
                {
                    'detail': (
                        f'Saldo insuficiente en caja. Disponible: '
                        f'${caja.saldo_actual:.2f}.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        movimiento = MovimientoCaja.objects.create(
            caja=caja,
            tipo_movimiento=movimiento_data['tipo_movimiento'],
            concepto=movimiento_data['concepto'],
            monto=monto,
        )
        return Response(
            MovimientoSerializer(movimiento).data,
            status=status.HTTP_201_CREATED,
        )
