from django.urls import path
from .views import (
    CategoriasAPIView,
    ProveedoresAPIView,
    InsumosAPIView,
    InsumosDetalleAPIView,
    InsumosListadoAPIView,
    ComprasAPIView,
)

urlpatterns = [
    path('categorias/', CategoriasAPIView.as_view(), name='api-categorias'),
    path('proveedores/', ProveedoresAPIView.as_view(), name='api-proveedores'),
    path('insumos/', InsumosAPIView.as_view(), name='api-insumos'),
    path('insumos/<int:pk>/', InsumosDetalleAPIView.as_view(), name='api-insumos-detalle'),
    path('insumos-listado/', InsumosListadoAPIView.as_view(), name='api-insumos-listado'),
    path('compras/', ComprasAPIView.as_view(), name='api-compras'),
]
