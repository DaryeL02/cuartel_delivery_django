from django.test import TestCase

from core.models import Producto
from .serializers import ProductoSerializer


class ProductoNameValidationTests(TestCase):
    def test_product_names_are_unique_case_insensitively(self):
        Producto.objects.create(
            nombre='Hamburguesa',
            precio_unitario='100.00',
            estado=True,
        )
        serializer = ProductoSerializer(data={
            'nombre': 'HAMBURGUESA',
            'precio_unitario': '120.00',
            'estado': True,
            'insumos': [],
        })

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['nombre'][0]),
            'Ya existe un registro con este nombre',
        )

    def test_existing_product_can_keep_its_name(self):
        producto = Producto.objects.create(
            nombre='Hamburguesa',
            precio_unitario='100.00',
            estado=True,
        )
        serializer = ProductoSerializer(instance=producto)

        self.assertEqual(serializer.validate_nombre('hamburguesa'), 'hamburguesa')
