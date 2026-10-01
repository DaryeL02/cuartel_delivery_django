from django.urls import path
from .views import EstadoAPIView
from .views import EmpleadosAPIView
from .views import InsumosAPIView

urlpatterns = [
    path('estado/', EstadoAPIView.as_view(), name='api-estado'),
    path('empleados/', EmpleadosAPIView.as_view(), name='api-empleados'),
    path('insumos/', InsumosAPIView.as_view(), name='api-Insumos'),
]
