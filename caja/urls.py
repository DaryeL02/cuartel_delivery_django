from django.urls import path
from .views import (
    CajasAPIView,
    CajasDetalleAPIView,
)

urlpatterns = [
    path('cajas/', CajasAPIView.as_view(), name='api-cajas'),
    path('cajas/<int:pk>/', CajasDetalleAPIView.as_view(), name='api-cajas-detalle'),
]
