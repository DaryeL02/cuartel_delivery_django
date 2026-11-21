from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum, Q
from decimal import Decimal
from core.models import Caja, MetodoPago, MovimientoCaja
from usuarios.serializers import EmpleadoSimplificadoSerializer


class MovimientoSerializer(serializers.ModelSerializer):
    caja_usuario = serializers.CharField(read_only=True, source='caja.usuario.usuario')
    venta_id = serializers.IntegerField(read_only=True)
    compra_id = serializers.IntegerField(read_only=True)
    metodo_detalle = serializers.SerializerMethodField()

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
            'metodo_detalle',
        ]

    def get_metodo_detalle(self, obj):
        transaccion = obj.venta or obj.compra
        metodo = transaccion.metodo if transaccion else obj.metodo
        return metodo.nombre if metodo else 'Efectivo'


class MovimientoManualSerializer(serializers.Serializer):
    caja = serializers.PrimaryKeyRelatedField(queryset=Caja.objects.all())
    metodo = serializers.PrimaryKeyRelatedField(
        queryset=MetodoPago.objects.all(), required=False, allow_null=True
    )
    tipo_movimiento = serializers.ChoiceField(choices=MovimientoCaja.TipoMovimiento.choices)
    concepto = serializers.CharField(max_length=50, trim_whitespace=True)
    monto = serializers.DecimalField(
        max_digits=9,
        decimal_places=2,
        min_value=Decimal('0.01'),
    )


class MovimientoManualEdicionSerializer(serializers.Serializer):
    tipo_movimiento = serializers.ChoiceField(choices=MovimientoCaja.TipoMovimiento.choices)
    concepto = serializers.CharField(max_length=50, trim_whitespace=True)
    monto = serializers.DecimalField(
        max_digits=9,
        decimal_places=2,
        min_value=Decimal('0.01'),
    )


class CajaSerializer(serializers.ModelSerializer):
    movimientos_asociados = MovimientoSerializer(many=True, read_only=True, source='movimientos')
    empleado_detalle = EmpleadoSimplificadoSerializer(read_only=True, source='usuario.empleado')
    usuario_nombre = serializers.CharField(read_only=True, source='usuario.usuario')
    local_nombre = serializers.CharField(read_only=True, source='local.nombre')
    es_mia = serializers.SerializerMethodField()
    saldo_esperado = serializers.SerializerMethodField()
    saldo_actual = serializers.SerializerMethodField()
    efectivo_esperado = serializers.SerializerMethodField()
    digital_esperado = serializers.SerializerMethodField()
    efectivo_cierre_anterior = serializers.SerializerMethodField()
    ajuste_apertura = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
        read_only=True,
    )
    efectivo_real = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.00'),
        required=False,
        allow_null=True,
    )
    digital_real = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Caja
        fields = [
            'id_cajas',
            'fecha_hora_apertura',
            'fecha_hora_cierre',
            'monto_apertura',
            'ajuste_apertura',
            'monto_cierre',
            'estado',
            'movimientos_asociados',
            'empleado_detalle',
            'usuario_nombre',
            'local_nombre',
            'es_mia',
            'saldo_esperado',
            'saldo_actual',
            'efectivo_esperado',
            'efectivo_cierre_anterior',
            'efectivo_real',
            'digital_esperado',
            'digital_real',
            'diferencia_total',
            'observaciones_cierre',
            'usuario',
            'local',
        ]
        extra_kwargs = {
            'usuario': {'required': False},
            'fecha_hora_cierre': {'read_only': True},
            'monto_cierre': {'read_only': True},
            'estado': {'read_only': True},
            'diferencia_total': {'read_only': True},
        }

    def validate_monto_apertura(self, value):
        if value < 0:
            raise serializers.ValidationError('El monto de apertura no puede ser negativo.')
        return value

    def get_es_mia(self, obj):
        request = self.context.get('request')
        return bool(request and obj.usuario_id == request.user.id_usuarios)

    def get_saldo_esperado(self, obj):
        if (
            obj.fecha_hora_cierre is not None
            and obj.efectivo_esperado is not None
            and obj.digital_esperado is not None
        ):
            return obj.efectivo_esperado + obj.digital_esperado

        return obj.saldo_actual

    def get_saldo_actual(self, obj):
        return obj.saldo_actual

    def get_montos_esperados(self, obj):
        if hasattr(obj, '_montos_esperados_arqueo'):
            return obj._montos_esperados_arqueo
        if (
            obj.fecha_hora_cierre is not None
            and obj.efectivo_esperado is not None
            and obj.digital_esperado is not None
        ):
            obj._montos_esperados_arqueo = (
                obj.efectivo_esperado,
                obj.digital_esperado,
            )
            return obj._montos_esperados_arqueo

        obj._montos_esperados_arqueo = obj.montos_esperados()
        return obj._montos_esperados_arqueo

    def get_efectivo_esperado(self, obj):
        return self.get_montos_esperados(obj)[0]

    def get_digital_esperado(self, obj):
        return self.get_montos_esperados(obj)[1]

    def get_efectivo_cierre_anterior(self, obj):
        return getattr(obj, 'efectivo_cierre_anterior', None)

    def validate(self, attrs):
        if self.instance is None:
            return attrs

        errores = {}
        for campo in ('efectivo_real', 'digital_real'):
            if attrs.get(campo) is None:
                errores[campo] = 'Este campo es obligatorio para cerrar la caja.'
        if errores:
            raise serializers.ValidationError(errores)

        efectivo_esperado, digital_esperado = self.get_montos_esperados(self.instance)
        diferencia_total = (
            attrs['efectivo_real'] - efectivo_esperado
            + attrs['digital_real'] - digital_esperado
        )
        observaciones = (attrs.get('observaciones_cierre') or '').strip()
        if diferencia_total != 0 and len(observaciones) < 10:
            raise serializers.ValidationError({
                'observaciones_cierre': (
                    'Explica la diferencia en al menos 10 caracteres.'
                )
            })
        attrs['observaciones_cierre'] = observaciones or None
        return attrs

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
        efectivo_esperado, digital_esperado = self.get_montos_esperados(instance)
        efectivo_real = validated_data['efectivo_real']
        digital_real = validated_data['digital_real']
        diferencia_total = (
            efectivo_real - efectivo_esperado
            + digital_real - digital_esperado
        )
        instance.efectivo_esperado = efectivo_esperado
        instance.efectivo_real = efectivo_real
        instance.digital_esperado = digital_esperado
        instance.digital_real = digital_real
        instance.diferencia_total = diferencia_total
        instance.observaciones_cierre = validated_data.get('observaciones_cierre')
        instance.monto_cierre = efectivo_real + digital_real
        instance.fecha_hora_cierre = timezone.now()
        instance.estado = False
        instance.save(update_fields=[
            'efectivo_esperado',
            'efectivo_real',
            'digital_esperado',
            'digital_real',
            'diferencia_total',
            'observaciones_cierre',
            'monto_cierre',
            'fecha_hora_cierre',
            'estado',
        ])
        return instance
