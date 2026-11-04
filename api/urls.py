from django.urls import path
from .views import *

urlpatterns = [
    path('estado/', EstadoAPIView.as_view(), name='api-estado'),
    path('empleados/', EmpleadosAPIView.as_view(), name='api-empleados'),
    path('empleados/<int:pk>/', EmpleadosDetalleAPIView.as_view(), name='api-empleados-detalle'),
    path('empleados/me/', PerfilAPIView.as_view(), name='api-perfil'),
    path('locales/', LocalesAPIView.as_view(), name='api-locales'),
    path('roles/', RolesAPIView.as_view(), name='api-roles'),
    path('insumos/', InsumosAPIView.as_view(), name='api-insumos'),
    path('insumos/<int:pk>/', InsumosDetalleAPIView.as_view(), name='api-insumos-detalle'),
    path('productos/', ProductosAPIView.as_view(), name='api-productos'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('categorias/', CategoriasAPIView.as_view(), name='api-categorias'),
    path('proveedores/', ProveedoresAPIView.as_view(), name='api-proveedores'),

    path('menus/', MenusAPIView.as_view(), name='api-menus'),
    
    
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='api-password-reset-confirm'),
]
