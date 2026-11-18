from django.test import TestCase
from rest_framework.test import APITestCase

from core.models import Bebida, Empleado, Local, Producto, Usuario


class PedidoBebidaApiTests(APITestCase):
    def setUp(self):
        usuario = Usuario.objects.create_user(
            usuario='pedido_test',
            email='pedido_test@example.com',
            password='test-password',
        )
        local = Local.objects.create(nombre='Sucursal test', direccion='Dirección test')
        self.empleado = Empleado.objects.create(
            local=local,
            dni='87654321',
            nombre='Ana',
            apellido='Pérez',
            telefono='12345678',
            estado=True,
        )
        self.bebida = Bebida.objects.create(
            nombre='Agua',
            precio_unitario='7.00',
            unidad='Unidades',
        )
        self.producto = Producto.objects.create(
            nombre='Hamburguesa',
            precio_unitario='3.00',
            estado=True,
        )
        self.client.force_authenticate(usuario)

    def test_pedido_creates_and_updates_beverage_details(self):
        response = self.client.post(
            '/api/pedidos/',
            {
                'empleado': self.empleado.pk,
                'cliente': 'Cliente test',
                'direccion': 'Mesa 1',
                'detalles': [{'id_bebidas': self.bebida.pk, 'cantidad': 2}],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data['precio_total'], '14.00')
        self.assertEqual(response.data['pedido_detalle'][0]['bebida']['id_bebidas'], self.bebida.pk)

        pedido_id = response.data['id_pedidos']
        actualizacion = self.client.patch(
            f'/api/pedidos/{pedido_id}/',
            {'detalles': [{'id_productos': self.producto.pk, 'cantidad': 3}]},
            format='json',
        )

        self.assertEqual(actualizacion.status_code, 200, actualizacion.data)
        self.assertEqual(actualizacion.data['precio_total'], '9.00')
        self.assertEqual(actualizacion.data['pedido_detalle'][0]['producto']['id_productos'], self.producto.pk)
        self.assertIsNone(actualizacion.data['pedido_detalle'][0]['bebida'])
