from django.urls import path
from .views import (
    PedidosAPIView,
    PedidosDetalleAPIView,
    MetodosDePagoAPIView,
    VentasAPIView,
    DetallesVentaAPIView,
)

urlpatterns = [
    path('pedidos/', PedidosAPIView.as_view(), name='api-pedidos'),
    path('pedidos/<int:pk>/', PedidosDetalleAPIView.as_view(), name='api-pedidos-detalle'),
    path('metodos/', MetodosDePagoAPIView.as_view(), name='api-metodos'),
    path('ventas/', VentasAPIView.as_view(), name='api-ventas'),
    path('detallesventa/', DetallesVentaAPIView.as_view(), name='api-detalles-venta'),
]
