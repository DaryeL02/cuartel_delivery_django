from django.db import transaction
from rest_framework import serializers
from core.models import (
    Categoria,
    DetalleMenu,
    Empleado,
    Insumo,
    Menu,
    Producto,
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