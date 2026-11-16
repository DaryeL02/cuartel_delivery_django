from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Caja
from .serializers import CajaSerializer


class CajasAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cajas = Caja.objects.all().select_related(
            'usuario__empleado'
        ).prefetch_related(
            'movimientos'
        )

        status_param = request.query_params.get('status', None)
        date_param = request.query_params.get('date', None)

        hoy = timezone.localdate()
        condicion_activa = Q(estado=True, fecha_hora_cierre__isnull=True)
        condicion_hoy = Q(fecha_hora_apertura__date=hoy) | Q(fecha_hora_cierre__date=hoy)

        if status_param == 'active' and date_param == 'today':
            cajas = cajas.filter(condicion_hoy | condicion_activa)
        elif status_param == 'active':
            cajas = cajas.filter(condicion_activa)
        elif date_param == 'today':
            cajas = cajas.filter(condicion_hoy)

        cajas = cajas.order_by('-estado', '-fecha_hora_apertura')

        serializer = CajaSerializer(cajas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CajaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CajasDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        caja = get_object_or_404(Caja, pk=pk)
        serializer = CajaSerializer(caja)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        caja = get_object_or_404(Caja, pk=pk)

        serializer = CajaSerializer(caja, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Caja actualizado", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
