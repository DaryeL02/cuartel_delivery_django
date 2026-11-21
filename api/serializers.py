from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from core.models import (
    Categoria,
    Compra,
    DetalleCompra,
    DetalleMenu,
    Empleado,
    Insumo,
    MetodoPago,
    Menu,
    Producto,
    Proveedor,
    ProveedorInsumo,
    Usuario,
)

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class DetalleMenuSerializer(serializers.ModelSerializer):
    producto_data = ProductoSerializer(source='producto', read_only=True)

    class Meta:
        model = DetalleMenu
        fields = (
            'id_detalles_menus',
            'producto',
            'producto_data',
            'cantidad',
            'descuento',
        )
        read_only_fields = ('id_detalles_menus',)

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La cantidad debe ser mayor que cero.')
        return value

    def validate_descuento(self, value):
        if value < 0:
            raise serializers.ValidationError('El descuento no puede ser negativo.')
        return value


class MenuSerializer(serializers.ModelSerializer):
    detalles = DetalleMenuSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = (
            'id_menus',
            'nombre',
            'estado',
            'fecha_hora_inicio',
            'fecha_hora_fin',
            'detalles',
        )
        read_only_fields = ('id_menus',)

    def validate(self, attrs):
        inicio = attrs.get(
            'fecha_hora_inicio',
            getattr(self.instance, 'fecha_hora_inicio', None),
        )
        fin = attrs.get('fecha_hora_fin', getattr(self.instance, 'fecha_hora_fin', None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError({
                'fecha_hora_fin': 'La fecha de fin debe ser posterior al inicio.'
            })

        detalles = attrs.get('detalles')
        if detalles is not None:
            productos = [detalle['producto'].pk for detalle in detalles]
            if len(productos) != len(set(productos)):
                raise serializers.ValidationError({
                    'detalles': 'No se puede repetir un producto en el mismo menú.'
                })
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        detalles = validated_data.pop('detalles', [])
        menu = Menu.objects.create(**validated_data)
        DetalleMenu.objects.bulk_create(
            [DetalleMenu(menu=menu, **detalle) for detalle in detalles]
        )
        return menu

    @transaction.atomic
    def update(self, instance, validated_data):
        detalles = validated_data.pop('detalles', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if detalles is not None:
            instance.detalles.all().delete()
            DetalleMenu.objects.bulk_create(
                [DetalleMenu(menu=instance, **detalle) for detalle in detalles]
            )
        return instance


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ProveedorInsumoSerializer(serializers.ModelSerializer):
    proveedor_data = ProveedorSerializer(source='proveedor', read_only=True)
    insumo_data = InsumoSerializer(source='insumo', read_only=True)

    class Meta:
        model = ProveedorInsumo
        fields = (
            'id_proveedores_insumos',
            'proveedor',
            'proveedor_data',
            'insumo',
            'insumo_data',
        )
        read_only_fields = ('id_proveedores_insumos',)


class DetalleCompraSerializer(serializers.ModelSerializer):
    insumo_data = InsumoSerializer(source='insumo', read_only=True)

    class Meta:
        model = DetalleCompra
        fields = (
            'id_detalles_compras',
            'insumo',
            'insumo_data',
            'cantidad',
            'subtotal',
        )
        read_only_fields = ('id_detalles_compras',)

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La cantidad debe ser mayor que cero.')
        return value

    def validate_subtotal(self, value):
        if value < 0:
            raise serializers.ValidationError('El subtotal no puede ser negativo.')
        return value


class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True)
    metodo_data = MetodoPagoSerializer(source='metodo', read_only=True)
    proveedor_data = ProveedorSerializer(source='proveedor', read_only=True)

    class Meta:
        model = Compra
        fields = (
            'id_compras',
            'metodo',
            'metodo_data',
            'proveedor',
            'proveedor_data',
            'precio_total',
            'monto_efectivo',
            'monto_transferencia',
            'fecha_hora_creacion',
            'detalles',
        )
        read_only_fields = ('id_compras', 'precio_total', 'fecha_hora_creacion')

    def validate_monto_efectivo(self, value):
        if value < 0:
            raise serializers.ValidationError('El monto en efectivo no puede ser negativo.')
        return value

    def validate_monto_transferencia(self, value):
        if value < 0:
            raise serializers.ValidationError('El monto por transferencia no puede ser negativo.')
        return value

    def validate(self, attrs):
        detalles = attrs.get('detalles')
        precio_total = (
            sum((detalle['subtotal'] for detalle in detalles), start=Decimal('0'))
            if detalles is not None
            else getattr(self.instance, 'precio_total', Decimal('0'))
        )
        monto_efectivo = attrs.get(
            'monto_efectivo',
            getattr(self.instance, 'monto_efectivo', Decimal('0')),
        )
        monto_transferencia = attrs.get(
            'monto_transferencia',
            getattr(self.instance, 'monto_transferencia', Decimal('0')),
        )
        if monto_efectivo + monto_transferencia > precio_total:
            raise serializers.ValidationError({
                'monto_efectivo': 'La suma de los pagos no puede superar el total de la compra.'
            })

        if detalles is not None:
            insumos = [detalle['insumo'].pk for detalle in detalles]
            if not insumos:
                raise serializers.ValidationError({
                    'detalles': 'La compra debe incluir al menos un insumo.'
                })
            if len(insumos) != len(set(insumos)):
                raise serializers.ValidationError({
                    'detalles': 'No se puede repetir un insumo en la misma compra.'
                })

            proveedor = attrs.get(
                'proveedor',
                getattr(self.instance, 'proveedor', None),
            )
            if proveedor:
                suministrados = set(
                    ProveedorInsumo.objects.filter(
                        proveedor=proveedor,
                        insumo_id__in=insumos,
                    ).values_list('insumo_id', flat=True)
                )
                if suministrados != set(insumos):
                    raise serializers.ValidationError({
                        'detalles': 'El proveedor no suministra uno o varios insumos seleccionados.'
                    })
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        precio_total = sum(
            (detalle['subtotal'] for detalle in detalles_data),
            start=Decimal('0'),
        )
        compra = Compra.objects.create(
            precio_total=precio_total,
            **validated_data,
        )
        for detalle in detalles_data:
            insumo = detalle['insumo']
            DetalleCompra.objects.create(compra=compra, **detalle)
            insumo.stock_actual += detalle['cantidad']
            insumo.save(update_fields=['stock_actual'])
        return compra

    @transaction.atomic
    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if detalles_data is not None:
            for detalle in instance.detalles.select_related('insumo'):
                detalle.insumo.stock_actual -= detalle.cantidad
                detalle.insumo.save(update_fields=['stock_actual'])
            instance.detalles.all().delete()

            precio_total = sum(
                (detalle['subtotal'] for detalle in detalles_data),
                start=Decimal('0'),
            )
            for detalle in detalles_data:
                insumo = detalle['insumo']
                DetalleCompra.objects.create(compra=instance, **detalle)
                insumo.stock_actual += detalle['cantidad']
                insumo.save(update_fields=['stock_actual'])
            instance.precio_total = precio_total

        instance.save()
        return instance