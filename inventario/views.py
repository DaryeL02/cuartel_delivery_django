from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from core.pagination import PageSize20Pagination
from core.models import Insumo, Categoria, Proveedor, Compra, Bebida
from .serializers import (
    InsumoSerializer,
    InsumoSimplificadoSerializer,
    CategoriaSerializer,
    ProveedorSerializer,
    CompraSerializer,
    BebidaSerializer,
)


# --------------------------------- #
#              INSUMOS              #
# --------------------------------- #

class InsumosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        insumos = Insumo.objects.all().select_related(
            'categoria'
        ).prefetch_related(
            'proveedores_insumos__proveedor'
        )

        serializer = InsumoSerializer(insumos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InsumoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsumosDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)
        serializer = InsumoSerializer(insumo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)

        serializer = InsumoSerializer(insumo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Insumo actualizado", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)
        insumo.delete()
        return Response("Insumo eliminado", status=status.HTTP_200_OK)


class InsumosListadoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        insumos = Insumo.objects.all()
        serializer = InsumoSimplificadoSerializer(insumos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriasAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProveedorViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    pagination_class = None


class BebidaViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Bebida.objects.all()
    serializer_class = BebidaSerializer
    pagination_class = None


# --------------------------------- #
#              COMPRAS              #
# --------------------------------- #

class CompraViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CompraSerializer
    pagination_class = PageSize20Pagination
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        compras = Compra.objects.all().select_related(
            'proveedor', 'metodo'
        ).prefetch_related(
            'detalles__insumo',
            'detalles__bebida',
            'movimientos_caja__caja',
        ).order_by('-fecha_hora_creacion', '-id_compras')
        proveedor = self.request.query_params.get('proveedor')
        desde = self.request.query_params.get('fecha_desde') or self.request.query_params.get('desde')
        hasta = self.request.query_params.get('fecha_hasta') or self.request.query_params.get('hasta')
        caja_id = self.request.query_params.get('id_cajas')
        if proveedor:
            compras = compras.filter(proveedor_id=proveedor)
        if desde:
            compras = compras.filter(fecha_hora_creacion__date__gte=desde)
        if hasta:
            compras = compras.filter(fecha_hora_creacion__date__lte=hasta)
        if caja_id:
            compras = compras.filter(movimientos_caja__caja_id=caja_id).distinct()
        return compras
