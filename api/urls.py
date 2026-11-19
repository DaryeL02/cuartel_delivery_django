from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('menus', MenuViewSet, basename='menu')

urlpatterns = [
    
    path('estado/', EstadoAPIView.as_view(), name='api-estado'),
    path('', include('usuarios.urls')),
    path('', include('inventario.urls')),
    path('', include('catalogo.urls')),
    path('', include('caja.urls')),
    path('', include('operaciones.urls')),
    
    path('empleados/', EmpleadosAPIView.as_view(), name='api-empleados'),

    path('empleados/<int:pk>/', EmpleadosDetalleAPIView.as_view(), name='api-empleados-detalle'),
    path('empleados/me/', PerfilAPIView.as_view(), name='api-perfil'),
    path('roles/', RolesAPIView.as_view(), name='api-roles'),
    path('locales/', LocalesAPIView.as_view(), name='api-locales'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),   
    
    path('categorias/', CategoriasAPIView.as_view(), name='api-categorias'),
    path('proveedores/', ProveedoresAPIView.as_view(), name='api-proveedores'),
    path('insumos/', InsumosAPIView.as_view(), name='api-insumos'),
    path('insumos/<int:pk>/', InsumosDetalleAPIView.as_view(), name='api-insumos-detalle'),
    
    path('productos/', ProductosAPIView.as_view(), name='api-productos'),
    path('cajas/', CajasAPIView.as_view(), name='api-cajas'),
    
    path('metodos/', MetodosDePagoAPIView.as_view(), name='api-metodos'),
    path('ventas/', VentasAPIView.as_view(), name='api-ventas'),
    path('detallesventa/', DetallesVentaAPIView.as_view(), name='api-ventas'),
    
    path('compras/', ComprasAPIView.as_view(), name='api-compras'),
    
    path('pedidos/', PedidosAPIView.as_view(), name='api-pedidos'),

    path('dashboard/', DashboardAPIView.as_view(), name='api-dashboard'),
    
    # Cambio de clave #
    
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='api-password-reset-confirm'),
    
    path('', include(router.urls)),
    

]


