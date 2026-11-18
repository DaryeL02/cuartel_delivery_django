from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Pedido, Venta, DetalleVenta, MetodoPago
from .serializers import (
    PedidoSerializer,
    VentaSerializer,
    DetalleVentaSerializer,
    MetodoPagoSerializer,
)


# --------------------------------- #
#              PEDIDOS              #
# --------------------------------- #

class PedidosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pedidos = Pedido.objects.all().select_related(
            'empleado'
        ).prefetch_related(
            'detalles__producto', 'detalles__bebida'
        )

        date_param = request.query_params.get('date', None)
        pagado_param = request.query_params.get('pagado', None)

        if date_param == 'today':
            hoy = date.today()
            pedidos = pedidos.filter(fecha_hora_creacion__date=hoy)

        if pagado_param is not None:
            es_pagado = pagado_param.lower() == 'true'
            pedidos = pedidos.filter(pagado=es_pagado)

        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PedidoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidosDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)

        serializer = PedidoSerializer(pedido, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        detalles = DetalleVenta.objects.all().select_related('producto')
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VentasAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ventas = Venta.objects.all().select_related(
            'metodo'
        ).prefetch_related(
            'detalles__producto', 'detalles__bebida'
        )
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')
        if desde:
            ventas = ventas.filter(fecha_hora_creacion__date__gte=desde)
        if hasta:
            ventas = ventas.filter(fecha_hora_creacion__date__lte=hasta)

        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VentaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
