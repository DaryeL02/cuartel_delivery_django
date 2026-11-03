from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Empleado, Insumo, Producto, Usuario, Categoria, Proveedor, ProveedorInsumo, Rol, Local
from .serializers import EmpleadoSerializer, InsumoSerializer, ProductoSerializer, UsuarioSerializer, CategoriaSerializer, ProveedorSerializer, LocalSerializer, RolSerializer
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
         
class EmpleadosAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        empleados = Empleado.objects.all().select_related(
            'local', 'usuario'
        ).prefetch_related(
            'usuario__usuarios_roles__rol'
        )
        
        serializer = EmpleadoSerializer(empleados, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Clonamos o limpiamos el request.data si 'local' viene como string vacío
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        if data.get('local') == "":
            data['local'] = None

        serializer = EmpleadoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class EmpleadosDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        empleado = get_object_or_404(Empleado, pk=pk)
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        empleado = get_object_or_404(Empleado, pk=pk)
        
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        if data.get('local') == "":
            data['local'] = None

        # Pasamos la instancia existente para que ejecute el método 'update'
        serializer = EmpleadoSerializer(empleado, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        empleado = get_object_or_404(Empleado, pk=pk)
        
        empleado.delete()
        
        return Response("Empleado eliminado",status=status.HTTP_204_NO_CONTENT)
    
class LocalesAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        locales = Local.objects.all()
        
        serializer = LocalSerializer(locales, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RolesAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        roles = Rol.objects.all()
        
        serializer = RolSerializer(roles, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
                
        return Response("Error al actualizar insumo",status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        insumo = get_object_or_404(Insumo, pk=pk)
        
        insumo.delete()
        
        return Response("Insumo eliminado",status=status.HTTP_204_NO_CONTENT)
 
class CategoriasAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        categorias = Categoria.objects.all()
        
        serializer = CategoriaSerializer(categorias, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductosAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        productos = Producto.objects.all()
        
        serializer = ProductoSerializer(productos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProveedoresAPIView(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        proveedores = Proveedor.objects.all()
        
        serializer = ProveedorSerializer(proveedores, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
