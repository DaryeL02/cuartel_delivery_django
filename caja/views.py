from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import DecimalField, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.db import IntegrityError, transaction
from decimal import Decimal
from rest_framework.authtoken.models import Token

from core.models import Caja, MovimientoCaja, Pedido
from core.permissions import RoleBasedIsAuthenticated
from .serializers import (
    CajaSerializer,
    MovimientoManualEdicionSerializer,
    MovimientoManualSerializer,
    MovimientoSerializer,
)


def _efectivo_cierre_anterior(local_id):
    caja_anterior = Caja.objects.filter(
        local_id=local_id,
        fecha_hora_cierre__isnull=False,
    ).order_by('-fecha_hora_cierre', '-id_cajas').first()
    if caja_anterior is None:
        return None

    for valor in (
        caja_anterior.efectivo_real,
        caja_anterior.efectivo_esperado,
        caja_anterior.monto_cierre,
        caja_anterior.monto_apertura,
    ):
        if valor is not None:
            return valor
    return None


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
        efectivo_cierre_anterior = Caja.objects.filter(
            local_id=OuterRef('local_id'),
            fecha_hora_cierre__isnull=False,
            fecha_hora_cierre__lte=OuterRef('fecha_hora_apertura'),
        ).order_by(
            '-fecha_hora_cierre',
            '-id_cajas',
        ).annotate(
            efectivo_final=Coalesce(
                'efectivo_real',
                'efectivo_esperado',
                'monto_cierre',
                'monto_apertura',
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        ).values('efectivo_final')[:1]
        cajas = cajas.annotate(
            efectivo_cierre_anterior=Subquery(
                efectivo_cierre_anterior,
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )

        status_param = request.query_params.get('status', None)
        date_param = request.query_params.get('date', None)
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        local_id = request.query_params.get('local')
        solo_cerradas = request.query_params.get('solo_cerradas') == 'true'
        if local_id:
            cajas = cajas.filter(local_id=local_id)
        if solo_cerradas:
            cajas = cajas.filter(estado=False, fecha_hora_cierre__isnull=False)

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

        if solo_cerradas:
            cajas = cajas.order_by('-fecha_hora_cierre', '-id_cajas')
        elif local_id:
            cajas = cajas.order_by('-fecha_hora_apertura', '-id_cajas')
        else:
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
        justificacion_apertura = datos.get('justificacion_apertura', '') or ''
        datos.pop('justificacion_apertura', None)
        if not isinstance(justificacion_apertura, str):
            return Response(
                {'justificacion_apertura': 'La justificación debe ser texto.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        justificacion_apertura = justificacion_apertura.strip()
        datos['usuario'] = request.user.id_usuarios
        serializer = CajaSerializer(data=datos, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        local_id = serializer.validated_data['local'].id_locales
        monto_apertura_solicitado = serializer.validated_data['monto_apertura']
        efectivo_anterior = _efectivo_cierre_anterior(local_id)
        monto_apertura_base = (
            efectivo_anterior if efectivo_anterior is not None else Decimal('0.00')
        )
        diferencia_apertura = monto_apertura_solicitado - monto_apertura_base
        if diferencia_apertura and not justificacion_apertura:
            return Response(
                {
                    'justificacion_apertura': (
                        'Debes justificar la diferencia respecto al saldo base de apertura.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(justificacion_apertura) > 50:
            return Response(
                {'justificacion_apertura': 'La justificación no puede superar 50 caracteres.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.validated_data['monto_apertura'] = monto_apertura_base
        caja_abierta = Caja.objects.filter(
            local_id=local_id,
        ).filter(Q(estado=True) | Q(fecha_hora_cierre__isnull=True)).exists()

        if caja_abierta:
            return Response(
                {"detail": "Ya existe una caja abierta en el local."},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            with transaction.atomic():
                caja = serializer.save()
                caja.ajuste_apertura = diferencia_apertura if diferencia_apertura else None
                caja.save(update_fields=['ajuste_apertura'])
                if diferencia_apertura:
                    MovimientoCaja.objects.create(
                        caja=caja,
                        tipo_movimiento=(
                            MovimientoCaja.TipoMovimiento.INGRESO
                            if diferencia_apertura > 0
                            else MovimientoCaja.TipoMovimiento.EGRESO
                        ),
                        concepto=justificacion_apertura,
                        monto=abs(diferencia_apertura),
                    )
        except IntegrityError:
            return Response(
                {"detail": "Ya existe una caja abierta en el local."},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(
            CajaSerializer(caja, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


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

        pedidos_del_local = Pedido.objects.filter(empleado__local_id=caja.local_id)
        pedidos_en_proceso = pedidos_del_local.filter(
            estado=Pedido.Estado.EN_PROCESO
        ).count()
        pedidos_impagos = pedidos_del_local.exclude(
            estado=Pedido.Estado.CANCELADO
        ).filter(pagado=False).count()
        if pedidos_en_proceso or pedidos_impagos:
            motivos = []
            if pedidos_en_proceso:
                motivos.append(
                    f'{pedidos_en_proceso} '
                    f'{"pedido" if pedidos_en_proceso == 1 else "pedidos"} en proceso'
                )
            if pedidos_impagos:
                motivos.append(
                    f'{pedidos_impagos} '
                    f'{"pedido no cancelado sin pagar" if pedidos_impagos == 1 else "pedidos no cancelados sin pagar"}'
                )
            return Response(
                {
                    'detail': (
                        'No se puede cerrar la caja: '
                        f'{" y ".join(motivos)}. Revísalos desde el historial de pedidos.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.data.get('confirmar_cierre') is not True:
            return Response(
                {"detail": "Debes confirmar explícitamente el cierre de caja."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        password = request.data.get('password')
        if not isinstance(password, str) or not password:
            return Response(
                {'password': 'Debes ingresar tu contraseña para cerrar la caja.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.user.check_password(password):
            return Response(
                {'password': 'La contraseña ingresada es incorrecta.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        datos = request.data.copy()
        datos.pop('password', None)
        serializer = CajaSerializer(
            caja, data=datos, partial=True, context={'request': request}
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
        metodo = movimiento_data.get('metodo')
        efectivo_esperado, digital_esperado = caja.montos_esperados()
        saldo_disponible = (
            efectivo_esperado
            if not metodo or 'efectivo' in metodo.nombre.casefold()
            else digital_esperado
        )
        if (
            movimiento_data['tipo_movimiento'] == MovimientoCaja.TipoMovimiento.EGRESO
            and monto > saldo_disponible
        ):
            return Response(
                {
                    'detail': (
                        f'Saldo insuficiente en caja. Disponible: '
                        f'${saldo_disponible:.2f}.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        movimiento = MovimientoCaja.objects.create(
            caja=caja,
            metodo=metodo,
            tipo_movimiento=movimiento_data['tipo_movimiento'],
            concepto=movimiento_data['concepto'],
            monto=monto,
        )
        return Response(
            MovimientoSerializer(movimiento).data,
            status=status.HTTP_201_CREATED,
        )


class MovimientoCajaDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [RoleBasedIsAuthenticated]

    @transaction.atomic
    def patch(self, request, pk):
        movimiento = get_object_or_404(
            MovimientoCaja.objects.select_for_update(),
            pk=pk,
        )
        caja = Caja.objects.select_for_update().get(pk=movimiento.caja_id)

        if movimiento.venta_id is not None or movimiento.compra_id is not None:
            return Response(
                {'detail': 'Solo se pueden editar movimientos manuales.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if caja.usuario_id != request.user.id_usuarios:
            return Response(
                {'detail': 'Solo puedes editar movimientos de una caja asignada a tu usuario.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not caja.estado or caja.fecha_hora_cierre is not None:
            return Response(
                {'detail': 'Solo puedes editar movimientos de una caja abierta.'},
                status=status.HTTP_409_CONFLICT,
            )

        campos_permitidos = {'tipo_movimiento', 'concepto', 'monto'}
        if set(request.data.keys()) - campos_permitidos:
            return Response(
                {'detail': 'Solo puedes modificar el tipo, concepto y monto del movimiento.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MovimientoManualEdicionSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        cambios = serializer.validated_data
        if not cambios:
            return Response(
                {'detail': 'Indica al menos un campo para actualizar.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tipo_movimiento = cambios.get('tipo_movimiento', movimiento.tipo_movimiento)
        monto = cambios.get('monto', movimiento.monto)
        if tipo_movimiento == MovimientoCaja.TipoMovimiento.EGRESO:
            efectivo, digital = caja.montos_esperados()
            metodo_nombre = movimiento.metodo.nombre.casefold() if movimiento.metodo else 'efectivo'
            saldo_categoria = efectivo if 'efectivo' in metodo_nombre else digital
            importe_anterior = (
                movimiento.monto
                if movimiento.tipo_movimiento == MovimientoCaja.TipoMovimiento.INGRESO
                else -movimiento.monto
            )
            saldo_sin_movimiento = saldo_categoria - importe_anterior
            if monto > saldo_sin_movimiento:
                return Response(
                    {
                        'detail': (
                            f'Saldo insuficiente en caja. Disponible: '
                            f'${saldo_sin_movimiento:.2f}.'
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        for campo, valor in cambios.items():
            setattr(movimiento, campo, valor)
        movimiento.save(update_fields=list(cambios))
        return Response(
            MovimientoSerializer(movimiento).data,
            status=status.HTTP_200_OK,
        )
