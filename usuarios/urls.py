from django.urls import path
from .views import (
    EmpleadosAPIView,
    EmpleadosDetalleAPIView,
    PerfilAPIView,
    RolesAPIView,
    LocalesAPIView,
    LoginAPIView,
    RegisterAPIView,
    UsuariosAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
)

urlpatterns = [
    path('empleados/', EmpleadosAPIView.as_view(), name='api-empleados'),
    path('empleados/<int:pk>/', EmpleadosDetalleAPIView.as_view(), name='api-empleados-detalle'),
    path('empleados/me/', PerfilAPIView.as_view(), name='api-perfil'),
    path('roles/', RolesAPIView.as_view(), name='api-roles'),
    path('locales/', LocalesAPIView.as_view(), name='api-locales'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('usuarios/', UsuariosAPIView.as_view(), name='api-usuarios'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='api-password-reset-confirm'),
]
