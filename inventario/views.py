from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Insumo, Categoria, Proveedor, Compra
from .serializers import (
    InsumoSerializer,
    InsumoSimplificadoSerializer,
    CategoriaSerializer,
    ProveedorSerializer,
    CompraSerializer,
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


class ProveedoresAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        proveedores = Proveedor.objects.all()
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------------------- #
#              COMPRAS              #
# --------------------------------- #

class ComprasAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        compras = Compra.objects.all().prefetch_related(
            'detalles__insumo'
        )

        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
