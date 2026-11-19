from datetime import timedelta

from django.test import TestCase
from rest_framework.test import APITestCase

from django.utils import timezone

from core.models import (
    Caja,
    Bebida,
    Empleado,
    Local,
    MetodoPago,
    MovimientoCaja,
    Pedido,
    Producto,
    Usuario,
    Venta,
)


class PedidoBebidaApiTests(APITestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            usuario='pedido_test',
            email='pedido_test@example.com',
            password='test-password',
        )
        local = Local.objects.create(nombre='Sucursal test', direccion='Dirección test')
        self.empleado = Empleado.objects.create(
            local=local,
            usuario=self.usuario,
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
        self.client.force_authenticate(self.usuario)

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
        self.assertIsNone(response.data['pedido_detalle'][0]['producto'])

        pedido_id = response.data['id_pedidos']
        fuera_del_rango = self.client.get(
            '/api/pedidos/',
            {'fecha_desde': (timezone.localdate() + timedelta(days=1)).isoformat()},
        )
        self.assertEqual(fuera_del_rango.status_code, 200)
        self.assertEqual(fuera_del_rango.data['results'], [])

        dentro_del_rango = self.client.get(
            '/api/pedidos/',
            {
                'fecha_desde': timezone.localdate().isoformat(),
                'fecha_hasta': timezone.localdate().isoformat(),
            },
        )
        self.assertEqual(
            [item['id_pedidos'] for item in dentro_del_rango.data['results']],
            [pedido_id],
        )

        actualizacion = self.client.patch(
            f'/api/pedidos/{pedido_id}/',
            {'detalles': [{'id_productos': self.producto.pk, 'cantidad': 3}]},
            format='json',
        )

        self.assertEqual(actualizacion.status_code, 200, actualizacion.data)
        self.assertEqual(actualizacion.data['precio_total'], '9.00')
        self.assertEqual(actualizacion.data['pedido_detalle'][0]['producto']['id_productos'], self.producto.pk)
        self.assertIsNone(actualizacion.data['pedido_detalle'][0]['bebida'])

    def test_pedidos_list_is_paginated_at_twenty_records(self):
        Pedido.objects.bulk_create([
            Pedido(
                empleado=self.empleado,
                cliente=f'Cliente {indice}',
                direccion='',
                precio_total='1.00',
                estado=Pedido.Estado.EN_PROCESO,
            )
            for indice in range(21)
        ])

        primera_pagina = self.client.get('/api/pedidos/')
        segunda_pagina = self.client.get('/api/pedidos/', {'page': 2})

        self.assertEqual(primera_pagina.data['count'], 21)
        self.assertEqual(len(primera_pagina.data['results']), 20)
        self.assertEqual(len(segunda_pagina.data['results']), 1)

    def test_ventas_se_filtran_por_rango_y_caja_y_exponen_la_caja(self):
        metodo = MetodoPago.objects.create(nombre='Efectivo', estado=True)
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.empleado.local,
            monto_apertura='100.00',
        )
        otro_local = Local.objects.create(nombre='Otra sucursal', direccion='Otra dirección')
        otra_caja = Caja.objects.create(
            usuario=self.usuario,
            local=otro_local,
            monto_apertura='100.00',
        )

        for caja_item in (caja, otra_caja):
            response = self.client.post(
                '/api/ventas/',
                {
                    'caja': caja_item.pk,
                    'metodo': metodo.pk,
                    'detalles': [{'id_productos': self.producto.pk, 'cantidad': 1}],
                },
                format='json',
            )
            self.assertEqual(response.status_code, 201, response.data)

        for indice in range(20):
            venta = Venta.objects.create(metodo=metodo, precio_total='3.00')
            MovimientoCaja.objects.create(
                venta=venta,
                caja=caja,
                tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
                concepto=f'Venta #{venta.pk}',
                monto='3.00',
            )
            if indice == 0:
                MovimientoCaja.objects.create(
                    venta=venta,
                    caja=caja,
                    tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
                    concepto=f'Venta #{venta.pk} duplicada',
                    monto='3.00',
                )

        hoy = timezone.localdate().isoformat()
        ventas = self.client.get(
            '/api/ventas/',
            {'fecha_desde': hoy, 'fecha_hasta': hoy, 'id_cajas': caja.pk},
        )
        ventas_pagina_dos = self.client.get(
            '/api/ventas/',
            {'fecha_desde': hoy, 'fecha_hasta': hoy, 'id_cajas': caja.pk, 'page': 2},
        )

        self.assertEqual(ventas.status_code, 200)
        self.assertEqual(ventas.data['count'], 21)
        self.assertEqual(len(ventas.data['results']), 20)
        self.assertEqual(len(ventas_pagina_dos.data['results']), 1)
        self.assertEqual(ventas.data['results'][0]['caja_detalle']['id_cajas'], caja.pk)
        self.assertEqual(ventas.data['results'][0]['caja_detalle']['usuario'], 'pedido_test')
        self.assertEqual(
            ventas.data['results'][0]['caja_detalle']['empleado_nombre'],
            'Ana Pérez',
        )
