from django.urls import path
from .views import *

urlpatterns = [
    path('estado/', EstadoAPIView.as_view(), name='api-estado'),
    path('empleados/', EmpleadosAPIView.as_view(), name='api-empleados'),
    path('insumos/', InsumosAPIView.as_view(), name='api-pnsumos'),
    path('productos/', ProductosAPIView.as_view(), name='api-productos'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('categorias/', CategoriasAPIView.as_view(), name='api-categorias'),
]
