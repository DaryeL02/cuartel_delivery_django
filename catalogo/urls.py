from django.urls import path
from .views import (
    ProductosAPIView,
    ProductosDetalleAPIView,
    ProductosListadoAPIView,
    MenusAPIView,
)

urlpatterns = [
    path('productos/', ProductosAPIView.as_view(), name='api-productos'),
    path('productos/<int:pk>/', ProductosDetalleAPIView.as_view(), name='api-productos-detalle'),
    path('productos-listado/', ProductosListadoAPIView.as_view(), name='api-productos-listado'),
    # path('menus/', MenusAPIView.as_view(), name='api-menus'),
]
