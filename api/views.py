from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import (
    Categoria,
    Empleado,
    Insumo,
    Menu,
    Producto,
    Usuario,
)
from .serializers import (
    CategoriaSerializer,
    EmpleadoSerializer,
    InsumoSerializer,
    MenuSerializer,
    ProductoSerializer,
    UsuarioSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework import viewsets


def is_menu_administrator(user):
    return user.is_authenticated and (
        user.is_staff
        or user.is_superuser
        or user.usuarios_roles.filter(
            rol__nombre__iexact='Administrador',
            rol__estado=True,
        ).exists()
    )


class IsMenuAdministrator(BasePermission):
    def has_permission(self, request, view):
        return is_menu_administrator(request.user)


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


class MenuPermissionsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'is_admin': is_menu_administrator(request.user)})


class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        email = str(request.data.get('email', '')).strip()
        user = Usuario.objects.filter(email__iexact=email, estado=True).first() if email else None

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = (
                f"{settings.FRONTEND_URL.rstrip('/')}/#/authentication/reset-password"
                f"?uid={uid}&token={token}"
            )
            try:
                send_mail(
                    'Restablecimiento de contraseña',
                    f"Hola {user.usuario}, usa este enlace para crear una nueva contraseña:\n\n"
                    f"{reset_url}\n\nSi no solicitaste este cambio, ignora este mensaje.",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                )
            except Exception:
                return Response(
                    {'detail': 'No se pudo enviar el correo. Revisa la configuración de email.'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

        return Response(
            {'detail': 'Si el correo está asociado a una cuenta, recibirás instrucciones.'},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        uid = request.data.get('uid', '')
        token = request.data.get('token', '')
        new_password = request.data.get('new_password', '')

        if not uid or not token or not new_password:
            return Response(
                {'detail': 'Faltan datos para restablecer la contraseña.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = Usuario.objects.get(pk=user_id, estado=True)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response(
                {'detail': 'El enlace no es válido o ya venció.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {'detail': 'El enlace no es válido o ya venció.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(new_password, user)
        except ValidationError as error:
            return Response(
                {'new_password': error.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=['password'])
        Token.objects.filter(user=user).delete()

        return Response(
            {'detail': 'La contraseña se restableció correctamente.'},
            status=status.HTTP_200_OK,
        )
    
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            user = Usuario.objects.create_user(
                usuario=validated_data['usuario'],
                password=validated_data['password'],
                email=validated_data.get('email') or None,
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
        
        insumos = Insumo.objects.all()
        
        serializer = InsumoSerializer(insumos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmpleadoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.prefetch_related('detalles__producto').all()
    serializer_class = MenuSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = self.permission_classes
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permissions = [IsAuthenticated, IsMenuAdministrator]
        return [permission() for permission in permissions]
