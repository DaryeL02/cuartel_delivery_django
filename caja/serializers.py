from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum, Q
from core.models import Caja, MovimientoCaja
from usuarios.serializers import EmpleadoSimplificadoSerializer


class MovimientoSerializer(serializers.ModelSerializer):
    caja_usuario = serializers.CharField(read_only=True, source='caja.usuario.usuario')
    venta_id = serializers.IntegerField(read_only=True)
    compra_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MovimientoCaja
        fields = [
            'id_movimientos',
            'tipo_movimiento',
            'concepto',
            'monto',
            'fecha_hora_creacion',
            'venta_id',
            'compra_id',
            'caja_usuario',
        ]


class CajaSerializer(serializers.ModelSerializer):
    movimientos_asociados = MovimientoSerializer(many=True, read_only=True, source='movimientos')
    empleado_detalle = EmpleadoSimplificadoSerializer(read_only=True, source='usuario.empleado')
    usuario_nombre = serializers.CharField(read_only=True, source='usuario.usuario')
    es_mia = serializers.SerializerMethodField()
    saldo_esperado = serializers.SerializerMethodField()

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
            'usuario_nombre',
            'es_mia',
            'saldo_esperado',
            'usuario',
            'local',
        ]
        extra_kwargs = {
            'usuario': {'required': False},
            'fecha_hora_cierre': {'read_only': True},
            'monto_cierre': {'read_only': True},
            'estado': {'read_only': True},
        }

    def validate_monto_apertura(self, value):
        if value < 0:
            raise serializers.ValidationError('El monto de apertura no puede ser negativo.')
        return value

    def get_es_mia(self, obj):
        request = self.context.get('request')
        return bool(request and obj.usuario_id == request.user.id_usuarios)

    def get_saldo_esperado(self, obj):
        totales = obj.movimientos.aggregate(
            ingresos=Sum('monto', filter=Q(tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO)),
            egresos=Sum('monto', filter=Q(tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO)),
        )
        return obj.monto_apertura + (totales['ingresos'] or 0) - (totales['egresos'] or 0)

    @transaction.atomic
    def create(self, validated_data):
        local = validated_data.get('local')
        if Caja.objects.filter(
            local=local,
        ).filter(Q(estado=True) | Q(fecha_hora_cierre__isnull=True)).exists():
            raise serializers.ValidationError({
                'detail': 'Ya existe una caja abierta en el local.'
            })
        nueva_caja = Caja.objects.create(**validated_data)
        return nueva_caja

    @transaction.atomic
    def update(self, instance, validated_data):
        movimientos = instance.movimientos.aggregate(
            ingresos=Sum('monto', filter=Q(tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO)),
            egresos=Sum('monto', filter=Q(tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO)),
        )
        instance.monto_cierre = (
            instance.monto_apertura
            + (movimientos['ingresos'] or 0)
            - (movimientos['egresos'] or 0)
        )
        instance.fecha_hora_cierre = timezone.now()
        instance.estado = False
        instance.save(update_fields=['monto_cierre', 'fecha_hora_cierre', 'estado'])
        return instance
