from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriasAPIView,
    InsumosAPIView,
    InsumosDetalleAPIView,
    InsumosListadoAPIView,
    CompraViewSet,
    ProveedorViewSet,
    BebidaViewSet,
)

router = DefaultRouter()
router.register('proveedores', ProveedorViewSet, basename='proveedor')
router.register('bebidas', BebidaViewSet, basename='bebida')
router.register('compras', CompraViewSet, basename='compra')

urlpatterns = [
    path('categorias/', CategoriasAPIView.as_view(), name='api-categorias'),
    path('insumos/', InsumosAPIView.as_view(), name='api-insumos'),
    path('insumos/<int:pk>/', InsumosDetalleAPIView.as_view(), name='api-insumos-detalle'),
    path('insumos-listado/', InsumosListadoAPIView.as_view(), name='api-insumos-listado'),
] + router.urls
