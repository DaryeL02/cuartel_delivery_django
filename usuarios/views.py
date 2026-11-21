from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated as AuthenticatedPermission

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from core.models import Usuario, Empleado, Local, Rol
from core.permissions import RoleBasedIsAuthenticated as IsAuthenticated
from .serializers import (
    UsuarioSerializer,
    UsuarioSimplificadoSerializer,
    EmpleadoSerializer,
    LocalSerializer,
    RolSerializer,
    PerfilUsuarioSerializer,
)


class LoginAPIView(APIView):
    def post(self, request):
        user = get_object_or_404(Usuario, usuario=request.data['usuario'])
        if not user.check_password(request.data['password']):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        serializer = UsuarioSimplificadoSerializer(instance=user)

        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)


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


class UsuariosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuarios = Usuario.objects.all()
        termino = request.query_params.get('search') or request.query_params.get('nombre')
        if termino:
            usuarios = usuarios.filter(
                Q(usuario__icontains=termino) | Q(email__icontains=termino)
            )
        serializer = UsuarioSimplificadoSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmpleadosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        empleados = Empleado.objects.all().select_related(
            'local', 'usuario'
        ).prefetch_related(
            'usuario__usuarios_roles__rol'
        )
        termino = request.query_params.get('search') or request.query_params.get('nombre')
        if termino:
            empleados = empleados.filter(
                Q(nombre__icontains=termino)
                | Q(apellido__icontains=termino)
                | Q(dni__icontains=termino)
                | Q(usuario__usuario__icontains=termino)
                | Q(usuario__usuarios_roles__rol__nombre__icontains=termino)
            ).distinct()
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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

        serializer = EmpleadoSerializer(empleado, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        empleado = get_object_or_404(Empleado, pk=pk)
        empleado.delete()
        return Response("Empleado eliminado", status=status.HTTP_204_NO_CONTENT)


class PerfilAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AuthenticatedPermission]

    def _respuesta_perfil(self, usuario):
        empleado = Empleado.objects.filter(usuario=usuario).select_related('local').first()
        return {
            'email': usuario.email,
            'empleado': EmpleadoSerializer(empleado).data if empleado else None,
        }

    def get(self, request):
        return Response(self._respuesta_perfil(request.user))

    def patch(self, request):
        serializer = PerfilUsuarioSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        usuario = serializer.save()
        return Response(self._respuesta_perfil(usuario), status=status.HTTP_200_OK)


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


class PasswordResetRequestAPIView(APIView):
    """
    Paso 1: Recibe el email, genera el token y envía el correo con el enlace de recuperación.
    """
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "El email es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        if not Usuario.objects.filter(email=email).exists():
            return Response(
                {"error": "El correo electrónico no está registrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        user = Usuario.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        frontend_origin = request.headers.get('Origin') or f"http://{request.get_host().split(':')[0]}:3000"
        reset_url = f"{frontend_origin}/#/authentication/change-password/{uid}/{token}/"

        subject = "Recuperación de contraseña"
        message = f"Hola {user.usuario},\n\nHas solicitado restablecer tu contraseña. Haz clic en el siguiente enlace:\n{reset_url}\n\nSi no lo solicitaste, ignora este mensaje."

        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            print(message)
        except Exception as e:
            print("ERROR REAL AL ENVIAR CORREO:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"mensaje": "Correo de recuperación enviado exitosamente."}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    """
    Paso 2: Valida el UID y el Token de la URL, y actualiza la contraseña.
    """
    def post(self, request, uidb64, token):
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"error": "La nueva contraseña es obligatoria"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"mensaje": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "El enlace de recuperación es inválido o ha expirado."}, status=status.HTTP_400_BAD_REQUEST)
