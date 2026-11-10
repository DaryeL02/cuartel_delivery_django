from django.urls import path
from .views import *

urlpatterns = [
    # USUARIOS/EMPLEADOS
    
    path('estado/', EstadoAPIView.as_view(), name='api-estado'),
    path('empleados/', EmpleadosAPIView.as_view(), name='api-empleados'),
    path('empleados/<int:pk>/', EmpleadosDetalleAPIView.as_view(), name='api-empleados-detalle'),
    path('empleados/me/', PerfilAPIView.as_view(), name='api-perfil'),
    path('roles/', RolesAPIView.as_view(), name='api-roles'),
    path('locales/', LocalesAPIView.as_view(), name='api-locales'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),   
    path('usuarios/', UsuariosAPIView.as_view(), name='api-usuarios'),
    
    path('categorias/', CategoriasAPIView.as_view(), name='api-categorias'),
    path('proveedores/', ProveedoresAPIView.as_view(), name='api-proveedores'),
    path('insumos/', InsumosAPIView.as_view(), name='api-insumos'),
    path('insumos/<int:pk>/', InsumosDetalleAPIView.as_view(), name='api-insumos-detalle'),
    path('insumos-listado/', InsumosListadoAPIView.as_view(), name='api-insumos-listado'),
    
    path('productos/', ProductosAPIView.as_view(), name='api-productos'),
    path('productos/<int:pk>/', ProductosDetalleAPIView.as_view(), name='api-productos-detalle'),
    path('cajas/', CajasAPIView.as_view(), name='api-cajas'),
    path('cajas/<int:pk>/', CajasDetalleAPIView.as_view(), name='api-cajas-detalle'),
    
    path('metodos/', MetodosDePagoAPIView.as_view(), name='api-metodos'),
    path('ventas/', VentasAPIView.as_view(), name='api-ventas'),
    path('detallesventa/', DetallesVentaAPIView.as_view(), name='api-ventas'),
    
    path('compras/', ComprasAPIView.as_view(), name='api-compras'),
    
    path('pedidos/', PedidosAPIView.as_view(), name='api-pedidos'),

    path('menus/', MenusAPIView.as_view(), name='api-menus'),
    
    # Cambio de clave #
    
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='api-password-reset-confirm'),
]
