from django.test import TestCase
from rest_framework.test import APITestCase
from core.models import (
    Bebida,
    Caja,
    Categoria,
    Insumo,
    Local,
    MetodoPago,
    MovimientoCaja,
    Proveedor,
    Usuario,
)


class CompraApiTests(APITestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            usuario='comprador_test',
            email='comprador_test@example.com',
            password='test-password',
        )
        self.local = Local.objects.create(nombre='Sucursal test', direccion='Dirección test')
        self.caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        self.metodo = MetodoPago.objects.create(nombre='Efectivo', estado=True)
        self.proveedor = Proveedor.objects.create(nombre='Proveedor test')
        self.categoria = Categoria.objects.create(nombre='Almacén')
        self.insumo = Insumo.objects.create(
            categoria=self.categoria,
            nombre='Harina',
            unidad='kg',
            stock_actual=4,
            stock_minimo=1,
        )
        self.bebida = Bebida.objects.create(
            nombre='Agua',
            precio_unitario='10.00',
            unidad='Unidades',
        )
        self.client.force_authenticate(self.usuario)

    def test_purchase_updates_stock_and_creates_cash_egress(self):
        response = self.client.post('/api/compras/', {
            'proveedor': self.proveedor.pk,
            'metodo': self.metodo.pk,
            'detalles': [
                {'insumo': self.insumo.pk, 'cantidad': 3, 'precio_unitario': '2.50'},
                {'bebida': self.bebida.pk, 'cantidad': 2, 'precio_unitario': '4.00'},
            ],
        }, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        self.insumo.refresh_from_db()
        self.bebida.refresh_from_db()
        self.assertEqual(self.insumo.stock_actual, 7)
        self.assertEqual(self.bebida.stock_actual, 2)
        self.assertEqual(response.data['precio_total'], '15.50')
        movimiento = MovimientoCaja.objects.get(compra_id=response.data['id_compras'])
        self.assertEqual(movimiento.tipo_movimiento, MovimientoCaja.TipoMovimiento.EGRESO)
        self.assertEqual(movimiento.caja_id, self.caja.pk)

    def test_purchase_rejects_empty_or_ambiguous_line_item(self):
        response = self.client.post('/api/compras/', {
            'proveedor': self.proveedor.pk,
            'metodo': self.metodo.pk,
            'detalles': [{
                'insumo': self.insumo.pk,
                'bebida': self.bebida.pk,
                'cantidad': 1,
                'precio_unitario': '1.00',
            }],
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data.get('id_compras'))
