from rest_framework import serializers
from django.db import transaction
from decimal import Decimal
from core.models import (
    Categoria,
    Proveedor,
    ProveedorInsumo,
    Insumo,
    Bebida,
    Compra,
    DetalleCompra,
    MetodoPago,
    Caja,
    MovimientoCaja,
)


# --------------------------------- #
#              INSUMOS              #
# --------------------------------- #

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id_categorias', 'nombre']


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id_proveedores', 'nombre', 'direccion', 'telefono', 'email', 'cuit', 'descripcion']


class ProveedorInsumoSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer()

    class Meta:
        model = ProveedorInsumo
        fields = ['id_proveedores_insumos', 'proveedor']


class InsumoSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = [
            'id_insumos',
            'nombre',
        ]


class InsumoSerializer(serializers.ModelSerializer):
    # Campos de Lectura (Para el GET del Frontend)
    categoria_detalle = CategoriaSerializer(read_only=True, source='categoria')
    proveedores_asociados = ProveedorInsumoSerializer(many=True, read_only=True, source='proveedores_insumos')

    # Campos de Escritura (Para el POST/PUT del Frontend)
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    proveedor = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all(), write_only=True, required=False)

    class Meta:
        model = Insumo
        fields = [
            'id_insumos',
            'nombre',
            'descripcion',
            'unidad',
            'stock_actual',
            'stock_minimo',
            'categoria',             # Escribir ID
            'proveedor',             # Escribir ID
            'categoria_detalle',     # Leer Objeto
            'proveedores_asociados', # Leer Lista
        ]

    def validate_nombre(self, value):
        insumos = Insumo.objects.filter(nombre__iexact=value)
        if self.instance:
            insumos = insumos.exclude(pk=self.instance.pk)
        if insumos.exists():
            raise serializers.ValidationError('Ya existe un registro con este nombre')
        return value

    def create(self, validated_data):
        proveedor_instancia = validated_data.pop('proveedor', None)
        insumo = Insumo.objects.create(**validated_data)
        if proveedor_instancia:
            ProveedorInsumo.objects.create(insumo=insumo, proveedor=proveedor_instancia)
        return insumo

    def update(self, instance, validated_data):
        proveedor_instancia = validated_data.pop('proveedor', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if proveedor_instancia is not None:
            ProveedorInsumo.objects.filter(insumo=instance).delete()
            ProveedorInsumo.objects.create(insumo=instance, proveedor=proveedor_instancia)
        return instance


class BebidaSerializer(serializers.ModelSerializer):
    unidad = serializers.CharField(default='unidades', required=False)

    class Meta:
        model = Bebida
        fields = [
            'id_bebidas', 'nombre', 'descripcion', 'estado', 'stock_actual',
            'stock_minimo', 'precio_unitario', 'unidad',
        ]

    def validate_nombre(self, value):
        bebidas = Bebida.objects.filter(nombre__iexact=value)
        if self.instance:
            bebidas = bebidas.exclude(pk=self.instance.pk)
        if bebidas.exists():
            raise serializers.ValidationError('Ya existe un registro con este nombre')
        return value


# --------------------------------- #
#              COMPRAS              #
# --------------------------------- #

class DetalleCompraSerializer(serializers.ModelSerializer):
    insumo = InsumoSimplificadoSerializer(read_only=True)
    bebida = BebidaSerializer(read_only=True)

    class Meta:
        model = DetalleCompra
        fields = [
            'id_detalles_compras',
            'cantidad',
            'subtotal',
            'insumo',
            'bebida',
        ]


class CompraDetalleEscrituraSerializer(serializers.Serializer):
    insumo = serializers.PrimaryKeyRelatedField(queryset=Insumo.objects.all(), required=False, allow_null=True)
    bebida = serializers.PrimaryKeyRelatedField(queryset=Bebida.objects.all(), required=False, allow_null=True)
    cantidad = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))

    def validate(self, attrs):
        if bool(attrs.get('insumo')) == bool(attrs.get('bebida')):
            raise serializers.ValidationError('Cada ítem debe ser un insumo o una bebida, pero no ambos.')
        return attrs


class CompraSerializer(serializers.ModelSerializer):
    proveedor_detalle = ProveedorSerializer(read_only=True, source='proveedor')
    metodo_detalle = serializers.StringRelatedField(read_only=True, source='metodo')
    detalle_compra = DetalleCompraSerializer(many=True, read_only=True, source='detalles')
    detalles = CompraDetalleEscrituraSerializer(many=True, write_only=True, allow_empty=False)
    proveedor = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all())
    metodo = serializers.PrimaryKeyRelatedField(queryset=MetodoPago.objects.all())
    precio_total = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)

    class Meta:
        model = Compra
        fields = [
            'id_compras',
            'precio_total',
            'fecha_hora_creacion',
            'proveedor',
            'proveedor_detalle',
            'metodo',
            'metodo_detalle',
            'detalle_compra',
            'detalles',
        ]

    def validate(self, attrs):
        limite = Decimal('9999999.99')
        detalles = attrs.get('detalles', [])
        total = sum(
            (detalle['precio_unitario'] * detalle['cantidad'] for detalle in detalles),
            Decimal('0.00'),
        )
        if total > limite:
            raise serializers.ValidationError({
                'detalles': 'El total de la compra supera el máximo permitido.'
            })
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        total = sum(
            (item['precio_unitario'] * item['cantidad'] for item in detalles_data),
            Decimal('0.00'),
        )
        caja_abierta = Caja.objects.select_for_update().filter(
            estado=True,
            fecha_hora_cierre__isnull=True,
        ).order_by('id_cajas').first()
        if caja_abierta is None:
            raise serializers.ValidationError({
                'detail': 'No hay una caja abierta para registrar la compra.'
            })
        if total > caja_abierta.saldo_actual:
            raise serializers.ValidationError({
                'detail': (
                    f'Saldo insuficiente en caja. Disponible: '
                    f'${caja_abierta.saldo_actual:.2f}.'
                )
            })

        compra = Compra.objects.create(precio_total=Decimal('0.00'), **validated_data)

        for item in detalles_data:
            cantidad = item['cantidad']
            subtotal = item['precio_unitario'] * cantidad
            insumo = item.get('insumo')
            bebida = item.get('bebida')
            if insumo:
                insumo_bloqueado = Insumo.objects.select_for_update().get(pk=insumo.pk)
                insumo_bloqueado.stock_actual += cantidad
                insumo_bloqueado.save(update_fields=['stock_actual'])
            else:
                bebida_bloqueada = Bebida.objects.select_for_update().get(pk=bebida.pk)
                bebida_bloqueada.stock_actual += cantidad
                bebida_bloqueada.save(update_fields=['stock_actual'])
            DetalleCompra.objects.create(
                compra=compra,
                insumo=insumo,
                bebida=bebida,
                cantidad=cantidad,
                subtotal=subtotal,
            )

        compra.precio_total = total
        compra.save(update_fields=['precio_total'])

        MovimientoCaja.objects.create(
            compra=compra,
            caja=caja_abierta,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO,
            concepto=f'Compra #{compra.id_compras}',
            monto=compra.precio_total,
        )
        return compra
