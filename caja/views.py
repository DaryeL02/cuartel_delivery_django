from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from django.db import IntegrityError, transaction
from rest_framework.authtoken.models import Token

from core.models import Caja, MovimientoCaja
from .serializers import CajaSerializer, MovimientoSerializer


class PuedeAbrirCaja(BasePermission):
    message = 'No tiene los permisos adecuados para abrir una caja'

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        return request.user.usuarios_roles.filter(
            Q(rol__nombre__iexact='Dueño')
            | Q(rol__nombre__iexact='Dueno')
            | Q(rol__nombre__iexact='Administrador')
        ).exists()


class CajasAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, PuedeAbrirCaja]

    def get(self, request):
        cajas = Caja.objects.all().select_related(
            'usuario__empleado'
        ).prefetch_related(
            'movimientos'
        )

        status_param = request.query_params.get('status', None)
        date_param = request.query_params.get('date', None)

        hoy = timezone.localdate()
        condicion_activa = Q(estado=True, fecha_hora_cierre__isnull=True)
        condicion_hoy = Q(fecha_hora_apertura__date=hoy) | Q(fecha_hora_cierre__date=hoy)

        if status_param == 'active' and date_param == 'today':
            cajas = cajas.filter(condicion_hoy | condicion_activa)
        elif status_param == 'active':
            cajas = cajas.filter(condicion_activa)
        elif date_param == 'today':
            cajas = cajas.filter(condicion_hoy)

        cajas = cajas.order_by('-estado', '-fecha_hora_apertura')

        serializer = CajaSerializer(cajas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        datos = request.data.copy()
        datos['usuario'] = request.user.id_usuarios
        serializer = CajaSerializer(data=datos, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        local_id = serializer.validated_data['local'].id_locales
        caja_abierta = Caja.objects.filter(
            local_id=local_id,
            estado=True,
            fecha_hora_cierre__isnull=True,
        ).exists()

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
    permission_classes = [IsAuthenticated]

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

        if not caja.estado or caja.fecha_hora_cierre is not None:
            return Response(
                {"detail": "Esta caja ya está cerrada."},
                status=status.HTTP_409_CONFLICT,
            )

        if request.data.get('confirmar_cierre') is not True:
            return Response(
                {"detail": "Debes confirmar explícitamente el cierre de caja."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CajaSerializer(caja, data={}, partial=True, context={'request': request})

        if serializer.is_valid():
            caja = serializer.save()
            return Response(CajaSerializer(caja, context={'request': request}).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        caja_abierta = Caja.objects.filter(
            usuario=request.user,
            estado=True,
            fecha_hora_cierre__isnull=True,
        ).exists()

        if caja_abierta:
            return Response(
                {"detail": "No puedes cerrar sesión mientras tengas una caja abierta."},
                status=status.HTTP_409_CONFLICT,
            )

        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_200_OK)


class MovimientosCajaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
