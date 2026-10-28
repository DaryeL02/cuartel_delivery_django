from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Empleado, Insumo, Producto, Usuario, Categoria, Proveedor, ProveedorInsumo
from .serializers import EmpleadoSerializer, InsumoSerializer, ProductoSerializer, UsuarioSerializer, CategoriaSerializer, ProveedorSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class EstadoAPIView(APIView):
    """
    Endpoint de ejemplo para confirmar que la API REST esta funcionando.

    Prueben visitarlo desde el navegador en:
        http://localhost:8000/api/estado/

    Sirve como punto de partida: reemplacen/amplien esta carpeta "api" con
    los serializers y vistas de los modelos reales de su organizacion
    (por ejemplo, ClienteSerializer, ClienteViewSet, etc.).
    """

    def get(self, request):
        return Response(
            {
                "estado": "ok",
                "mensaje": "La API REST del proyecto esta funcionando correctamente.",
            },
            status=status.HTTP_200_OK,
        )
   
class LoginAPIView(APIView):
    def post(self, request):
        user = get_object_or_404(Usuario, usuario=request.data['usuario'])
        if not user.check_password(request.data['password']):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        token, created  = Token.objects.get_or_create(user=user)
        serializer = UsuarioSerializer(instance=user)
        
             
        return Response({"token": token.key, "user":serializer.data}, status=status.HTTP_200_OK)
    
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            user = Usuario.objects.create_user(
                usuario=validated_data['usuario'],
                password=validated_data['password']
            )

            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
@authentication_classes ([TokenAuthentication])
@permission_classes ([IsAuthenticated])
class EmpleadosAPIView(APIView):
    
    def get(self, request):
        
        empleados = Empleado.objects.all()
        
        serializer = EmpleadoSerializer(empleados, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmpleadoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes ([TokenAuthentication])
@permission_classes ([IsAuthenticated])    
class InsumosAPIView(APIView):
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
    
    def put(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)

        serializer = InsumoSerializer(insumo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Insumo actualizado", status=status.HTTP_200_OK)
                
        return Response("Error al actualizar insumo",status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)
        
        insumo.delete()
        
        return Response("Insumo eliminado",status=status.HTTP_204_NO_CONTENT)
    
@authentication_classes ([TokenAuthentication])
@permission_classes ([IsAuthenticated])    
class CategoriasAPIView(APIView):
    def get(self, request):
        
        categorias = Categoria.objects.all()
        
        serializer = CategoriaSerializer(categorias, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@authentication_classes ([TokenAuthentication])
@permission_classes ([IsAuthenticated])  
class ProductosAPIView(APIView):
    def get(self, request):
        
        productos = Producto.objects.all()
        
        serializer = ProductoSerializer(productos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@authentication_classes ([TokenAuthentication])
@permission_classes ([IsAuthenticated])  
class ProveedoresAPIView(APIView):
    def get(self, request):
        
        proveedores = Proveedor.objects.all()
        
        serializer = ProveedorSerializer(proveedores, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
