from django.urls import path
from .views import (
    CajasAPIView,
    CajasDetalleAPIView,
    LogoutAPIView,
    MovimientosCajaAPIView,
)

urlpatterns = [
    path('cajas/', CajasAPIView.as_view(), name='api-cajas'),
    path('cajas/<int:pk>/', CajasDetalleAPIView.as_view(), name='api-cajas-detalle'),
    path('movimientos-caja/', MovimientosCajaAPIView.as_view(), name='api-movimientos-caja'),
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),
]
