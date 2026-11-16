from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from core.models import Caja, MovimientoCaja
from usuarios.serializers import EmpleadoSimplificadoSerializer


class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCaja
        fields = [
            'id_movimientos',
            'tipo_movimiento',
            'concepto',
            'monto',
        ]


class CajaSerializer(serializers.ModelSerializer):
    movimientos_asociados = MovimientoSerializer(many=True, read_only=True, source='movimientos')
    empleado_detalle = EmpleadoSimplificadoSerializer(read_only=True, source='usuario.empleado')
    caja = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Caja
        fields = [
            'id_cajas',
            'fecha_hora_apertura',
            'fecha_hora_cierre',
            'monto_apertura',
            'monto_cierre',
            'estado',
            'movimientos_asociados',
            'empleado_detalle',
            'usuario',
            'local',
            'caja',
        ]
        extra_kwargs = {
            'usuario': {'required': False},
            'local': {'required': False},
            'monto_apertura': {'required': False},
        }

    @transaction.atomic
    def create(self, validated_data):
        nueva_caja = Caja.objects.create(**validated_data)
        return nueva_caja

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data.pop('caja', None)

        instance.fecha_hora_cierre = timezone.now()
        instance.estado = False

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
