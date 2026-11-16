from rest_framework import serializers
from django.db import transaction
from core.models import (
    Producto,
    ProductoInsumo,
    Insumo,
    Menu,
    DetalleMenu,
)
from inventario.serializers import InsumoSimplificadoSerializer


# --------------------------------- #
#             PRODUCTOS             #
# --------------------------------- #

class ProductoSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id_productos',
            'nombre',
            'precio_unitario',
        ]


class ProductoInsumoSerializer(serializers.ModelSerializer):
    insumo = InsumoSimplificadoSerializer()

    class Meta:
        model = ProductoInsumo
        fields = ['id_productos_insumos', 'insumo']


class ProductoEscrituraDetalleSerializer(serializers.Serializer):
    id_insumos = serializers.PrimaryKeyRelatedField(queryset=Insumo.objects.all())


class ProductoSerializer(serializers.ModelSerializer):
    insumos_asociados = ProductoInsumoSerializer(many=True, read_only=True, source='productos_insumos')
    insumos = ProductoEscrituraDetalleSerializer(many=True, write_only=True)
    precio_unitario = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = Producto
        fields = [
            'id_productos',
            'nombre',
            'descripcion',
            'precio_unitario',
            'estado',
            'insumos_asociados',
            'insumos',
        ]

    @transaction.atomic
    def create(self, validated_data):
        insumos_data = validated_data.pop('insumos', [])
        nuevo_producto = Producto.objects.create(**validated_data)

        for item in insumos_data:
            insumo_instancia = item['id_insumos']
            ProductoInsumo.objects.create(
                producto=nuevo_producto,
                insumo=insumo_instancia,
            )

        return nuevo_producto

    @transaction.atomic
    def update(self, instance, validated_data):
        insumos_data = validated_data.pop('insumos', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if insumos_data is not None:
            ProductoInsumo.objects.filter(producto=instance).delete()

            for item in insumos_data:
                insumo_instancia = item['id_insumos']
                ProductoInsumo.objects.create(
                    producto=instance,
                    insumo=insumo_instancia,
                )

        return instance


# --------------------------------- #
#               MENÚS               #
# --------------------------------- #

class DetalleMenuSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = DetalleMenu
        fields = [
            'id_detalles_menus',
            'cantidad',
            'descuento',
            'producto',
        ]


class MenuSerializer(serializers.ModelSerializer):
    detalle_menu = DetalleMenuSerializer(many=True, read_only=True, source='detalles')

    class Meta:
        model = Menu
        fields = [
            'id_menus',
            'nombre',
            'estado',
            'detalle_menu',
        ]
