from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Empleado, Insumo
from .serializers import EmpleadoSerializer, InsumoSerializer


class EstadoAPIView(APIView):
    """
    Endpoint de ejemplo para confirmar que la API REST esta funcionando.

    Prueben visitarlo desde el navegador en:
        http://localhost:8000/api/estado/

    Sirve como punto de partida: reemplacen/amplien esta carpeta "api" con
    los serializers y vistas de los modelos reales de su organizacion
    (por ejemplo, ClienteSerializer, ClienteViewSet, etc.).
    """

    def get(self, request):
        return Response(
            {
                "estado": "ok",
                "mensaje": "La API REST del proyecto esta funcionando correctamente.",
            },
            status=status.HTTP_200_OK,
        )
        
class EmpleadosAPIView(APIView):
    def get(self, request):
        
        empleados = Empleado.objects.all()
        
        serializer = EmpleadoSerializer(empleados, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class InsumosAPIView(APIView):
    def get(self, request):
        
        insumos = Insumo.objects.all()
        
        serializer = InsumoSerializer(insumos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
            
