from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from core.models import Pedido, Venta, DetalleVenta, MetodoPago
from core.permissions import (
    RoleBasedIsAuthenticated as IsAuthenticated,
    get_active_role_names,
    is_full_access_user,
    is_operational_user,
)
from core.pagination import paginated_response
from .serializers import (
    PedidoSerializer,
    VentaSerializer,
    DetalleVentaSerializer,
    MetodoPagoSerializer,
)
from usuarios.serializers import EmpleadoSimplificadoSerializer


# --------------------------------- #
#              PEDIDOS              #
# --------------------------------- #

class PuedeAccederPedidos(IsAuthenticated):
    message = 'Los roles Planchero y Ayudante no pueden crear pedidos.'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        roles_restringidos = {'planchero', 'ayudante', 'ayudante de cocina'}
        return not (
            request.method == 'POST'
            and not is_full_access_user(request.user)
            and get_active_role_names(request.user).intersection(roles_restringidos)
        )


class PedidosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PuedeAccederPedidos]
    acceso_operativo_pedidos = True
    metodos_operativos_permitidos = {'GET', 'POST'}

    def get(self, request):
        pedidos = Pedido.objects.all().select_related(
            'empleado'
        ).prefetch_related(
            'detalles__producto',
            'detalles__bebida',
            'detalles__menu',
            'detalles__menu__detalles__producto',
            'detalles__menu__detalles__bebida',
        ).order_by('-fecha_hora_creacion', '-id_pedidos')

        date_param = request.query_params.get('date', None)
        pagado_param = request.query_params.get('pagado', None)
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')

        if date_param == 'today':
            hoy = date.today()
            pedidos = pedidos.filter(fecha_hora_creacion__date=hoy)
        if fecha_desde:
            pedidos = pedidos.filter(fecha_hora_creacion__date__gte=fecha_desde)
        if fecha_hasta:
            pedidos = pedidos.filter(fecha_hora_creacion__date__lte=fecha_hasta)

        if pagado_param is not None:
            es_pagado = pagado_param.lower() == 'true'
            pedidos = pedidos.filter(pagado=es_pagado)
        estado_param = request.query_params.get('estado')
        if estado_param:
            pedidos = pedidos.filter(estado=estado_param)

        return paginated_response(pedidos, PedidoSerializer, request)

    def post(self, request):
        data = request.data
        if is_operational_user(request.user):
            if (
                'mozo' in get_active_role_names(request.user)
                and data.get('estado') == Pedido.Estado.FINALIZADO
            ):
                return Response(
                    {'detail': 'El rol Mozo no puede crear pedidos como Finalizados.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            empleado = getattr(request.user, 'empleado', None)
            if empleado is None:
                return Response(
                    {'detail': 'Tu usuario no está asociado a un empleado para crear pedidos.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = request.data.copy()
            data['empleado'] = empleado.pk

        serializer = PedidoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidosDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    acceso_operativo_pedidos = True
    metodos_operativos_permitidos = {'GET', 'PATCH'}

    def get(self, request, pk):
        pedido = get_object_or_404(
            Pedido.objects.prefetch_related(
                'detalles__producto',
                'detalles__bebida',
                'detalles__menu',
                'detalles__menu__detalles__producto',
                'detalles__menu__detalles__bebida',
            ),
            pk=pk,
        )
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        if (
            request.data.get('estado') == Pedido.Estado.FINALIZADO
            and 'mozo' in get_active_role_names(request.user)
            and not is_full_access_user(request.user)
        ):
            return Response(
                {'detail': 'El rol Mozo no puede finalizar pedidos.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PedidoSerializer(pedido, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidosContextoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    acceso_operativo_pedidos = True
    metodos_operativos_permitidos = {'GET'}

    def get(self, request):
        empleado = getattr(request.user, 'empleado', None)
        return Response({
            'empleado': (
                EmpleadoSimplificadoSerializer(empleado).data if empleado else None
            )
        }, status=status.HTTP_200_OK)


# --------------------------------- #
#               VENTAS              #
# --------------------------------- #

class MetodosDePagoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        metodos = MetodoPago.objects.all()
        serializer = MetodoPagoSerializer(metodos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetallesVentaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        detalles = DetalleVenta.objects.all().select_related('producto', 'bebida', 'menu')
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VentasAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ventas = Venta.objects.all().select_related(
            'metodo'
        ).prefetch_related(
            'detalles__producto',
            'detalles__bebida',
            'detalles__menu',
            'detalles__menu__detalles__producto',
            'detalles__menu__detalles__bebida',
            'movimientos_caja__caja__local',
            'movimientos_caja__caja__usuario__empleado',
        ).order_by('-fecha_hora_creacion', '-id_ventas')
        desde = request.query_params.get('fecha_desde') or request.query_params.get('desde')
        hasta = request.query_params.get('fecha_hasta') or request.query_params.get('hasta')
        caja_id = request.query_params.get('id_cajas')
        if desde:
            ventas = ventas.filter(fecha_hora_creacion__date__gte=desde)
        if hasta:
            ventas = ventas.filter(fecha_hora_creacion__date__lte=hasta)
        if caja_id:
            ventas = ventas.filter(movimientos_caja__caja_id=caja_id).distinct()

        return paginated_response(ventas, VentaSerializer, request)

    def post(self, request):
        serializer = VentaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
