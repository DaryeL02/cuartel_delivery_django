from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('estado/', EstadoAPIView.as_view(), name='api-estado'),
    path('', include('usuarios.urls')),
    path('', include('inventario.urls')),
    path('', include('catalogo.urls')),
    path('', include('caja.urls')),
    path('', include('operaciones.urls')),
    
]
