from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from core.models import Producto, Menu
from core.permissions import RoleBasedIsAuthenticated as IsAuthenticated
from .serializers import (
    ProductoSerializer,
    ProductoSimplificadoSerializer,
    MenuSerializer,
)


# --------------------------------- #
#             PRODUCTOS             #
# --------------------------------- #

class ProductosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        productos = Producto.objects.all().prefetch_related(
            'productos_insumos__insumo'
        )
        termino = request.query_params.get('search') or request.query_params.get('nombre')
        if termino:
            productos = productos.filter(nombre__icontains=termino)

        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductosDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)

        serializer = ProductoSerializer(producto, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Producto actualizado", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return Response("Producto eliminado", status=status.HTTP_200_OK)


class ProductosListadoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    acceso_operativo_pedidos = True
    metodos_operativos_permitidos = {'GET'}

    def get(self, request):
        productos = Producto.objects.all()
        termino = request.query_params.get('search') or request.query_params.get('nombre')
        if termino:
            productos = productos.filter(nombre__icontains=termino)
        serializer = ProductoSimplificadoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------------------- #
#               MENÚS               #
# --------------------------------- #

class MenusAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        menus = Menu.objects.all().prefetch_related(
            'detalles'
        )

        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
