from rest_framework import serializers
from core.models import (
    Categoria,
    Proveedor,
    ProveedorInsumo,
    Insumo,
    Compra,
    DetalleCompra,
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
        fields = ['id_proveedores', 'nombre']


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


# --------------------------------- #
#              COMPRAS              #
# --------------------------------- #

class DetalleCompraSerializer(serializers.ModelSerializer):
    insumo = InsumoSimplificadoSerializer()

    class Meta:
        model = DetalleCompra
        fields = [
            'id_detalles_compras',
            'cantidad',
            'subtotal',
            'insumo',
        ]


class CompraSerializer(serializers.ModelSerializer):
    detalle_compra = DetalleCompraSerializer(many=True, read_only=True, source='detalles')

    class Meta:
        model = Compra
        fields = [
            'id_compras',
            'precio_total',
            'detalle_compra',
        ]
