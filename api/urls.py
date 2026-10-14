from django.urls import path
from .views import EstadoAPIView, EmpleadosAPIView, InsumosAPIView, ProductosAPIView

urlpatterns = [
    path('estado/', EstadoAPIView.as_view(), name='api-estado'),
    path('empleados/', EmpleadosAPIView.as_view(), name='api-empleados'),
    path('insumos/', InsumosAPIView.as_view(), name='api-insumos'),
    path('productos/', ProductosAPIView.as_view(), name='api-productos'),
]
