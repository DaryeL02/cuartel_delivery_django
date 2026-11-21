from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APITestCase

from django.utils import timezone

from core.models import (
    Caja,
    Bebida,
    Categoria,
    DetalleMenu,
    Empleado,
    Insumo,
    Local,
    Menu,
    MetodoPago,
    MovimientoCaja,
    Pedido,
    Producto,
    ProductoInsumo,
    Rol,
    Usuario,
    UsuarioRol,
    Venta,
)


class PedidoBebidaApiTests(APITestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            usuario='pedido_test',
            email='pedido_test@example.com',
            password='test-password',
        )
        rol_admin = Rol.objects.create(nombre='Administrador', estado=True)
        UsuarioRol.objects.create(usuario=self.usuario, rol=rol_admin)
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

    def test_cancelling_order_does_not_change_stock(self):
        self.bebida.stock_actual = 5
        self.bebida.save(update_fields=['stock_actual'])
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
        pedido_id = response.data['id_pedidos']

        cancelacion = self.client.patch(
            f'/api/pedidos/{pedido_id}/',
            {'estado': 'Cancelado'},
            format='json',
        )

        self.assertEqual(cancelacion.status_code, 200, cancelacion.data)
        self.bebida.refresh_from_db()
        self.assertEqual(self.bebida.stock_actual, 5)

    def test_orders_reject_inactive_menus_and_multiple_item_types(self):
        menu = Menu.objects.create(nombre='Menú inactivo', estado=False)
        inactive_menu = self.client.post(
            '/api/pedidos/',
            {
                'empleado': self.empleado.pk,
                'cliente': 'Cliente menú inactivo',
                'detalles': [{'id_menus': menu.pk, 'cantidad': 1}],
            },
            format='json',
        )
        multiple_items = self.client.post(
            '/api/pedidos/',
            {
                'empleado': self.empleado.pk,
                'cliente': 'Cliente con artículos duplicados',
                'detalles': [{
                    'id_productos': self.producto.pk,
                    'id_bebidas': self.bebida.pk,
                    'cantidad': 1,
                }],
            },
            format='json',
        )

        self.assertEqual(inactive_menu.status_code, 400, inactive_menu.data)
        self.assertEqual(multiple_items.status_code, 400, multiple_items.data)

    def test_selling_menu_calculates_price_and_decrements_composition_stock(self):
        categoria = Categoria.objects.create(nombre='Ingredientes')
        insumo = Insumo.objects.create(
            categoria=categoria,
            nombre='Pan de menú',
            unidad='kg',
            stock_actual='10.00',
            stock_minimo=0,
        )
        ProductoInsumo.objects.create(
            producto=self.producto,
            insumo=insumo,
            cantidad='0.50',
        )
        self.bebida.stock_actual = 10
        self.bebida.save(update_fields=['stock_actual'])
        menu = Menu.objects.create(nombre='Combo test', estado=True)
        DetalleMenu.objects.create(
            menu=menu,
            producto=self.producto,
            cantidad=2,
            descuento=10,
        )
        DetalleMenu.objects.create(
            menu=menu,
            bebida=self.bebida,
            cantidad=1,
            descuento=0,
        )
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.empleado.local,
            monto_apertura='100.00',
        )
        metodo = MetodoPago.objects.create(nombre='Efectivo', estado=True)

        response = self.client.post(
            '/api/ventas/',
            {
                'caja': caja.pk,
                'metodo': metodo.pk,
                'detalles': [{'id_menus': menu.pk, 'cantidad': 2}],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data['precio_total'], '24.80')
        self.assertEqual(response.data['detalle_venta'][0]['menu']['nombre'], 'Combo test')
        componentes_menu = response.data['detalle_venta'][0]['menu']['detalles']
        self.assertEqual(componentes_menu[0]['producto']['nombre'], self.producto.nombre)
        self.assertEqual(componentes_menu[0]['cantidad'], 2)
        self.assertEqual(componentes_menu[1]['bebida']['nombre'], self.bebida.nombre)
        self.assertEqual(componentes_menu[1]['cantidad'], 1)
        insumo.refresh_from_db()
        self.bebida.refresh_from_db()
        self.assertEqual(insumo.stock_actual, Decimal('8.00'))
        self.assertEqual(self.bebida.stock_actual, Decimal('8.00'))

    def test_finalizing_order_with_menu_decrements_stock_once(self):
        self.bebida.stock_actual = 10
        self.bebida.save(update_fields=['stock_actual'])
        menu = Menu.objects.create(nombre='Menú de bebida', estado=True)
        DetalleMenu.objects.create(
            menu=menu,
            bebida=self.bebida,
            cantidad=2,
            descuento=0,
        )
        response = self.client.post(
            '/api/pedidos/',
            {
                'empleado': self.empleado.pk,
                'cliente': 'Cliente menú',
                'direccion': 'Mesa 2',
                'detalles': [{'id_menus': menu.pk, 'cantidad': 3}],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data['precio_total'], '42.00')
        self.assertEqual(response.data['pedido_detalle'][0]['menu']['nombre'], menu.nombre)
        componentes_menu = response.data['pedido_detalle'][0]['menu']['detalles']
        self.assertEqual(componentes_menu[0]['bebida']['nombre'], self.bebida.nombre)
        self.assertEqual(componentes_menu[0]['cantidad'], 2)
        self.bebida.refresh_from_db()
        self.assertEqual(self.bebida.stock_actual, Decimal('10.00'))

        pedido_id = response.data['id_pedidos']
        finalizado = self.client.patch(
            f'/api/pedidos/{pedido_id}/',
            {'estado': 'Finalizado'},
            format='json',
        )
        self.assertEqual(finalizado.status_code, 200, finalizado.data)
        self.bebida.refresh_from_db()
        self.assertEqual(self.bebida.stock_actual, Decimal('4.00'))

        repetido = self.client.patch(
            f'/api/pedidos/{pedido_id}/',
            {'estado': 'Finalizado'},
            format='json',
        )
        self.assertEqual(repetido.status_code, 200, repetido.data)
        self.bebida.refresh_from_db()
        self.assertEqual(self.bebida.stock_actual, Decimal('4.00'))

    def test_selling_menu_with_insufficient_stock_rolls_back_sale(self):
        self.bebida.stock_actual = 1
        self.bebida.save(update_fields=['stock_actual'])
        menu = Menu.objects.create(nombre='Menú sin stock suficiente', estado=True)
        DetalleMenu.objects.create(
            menu=menu,
            bebida=self.bebida,
            cantidad=2,
            descuento=0,
        )
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.empleado.local,
            monto_apertura='100.00',
        )
        metodo = MetodoPago.objects.create(nombre='Efectivo', estado=True)

        response = self.client.post(
            '/api/ventas/',
            {
                'caja': caja.pk,
                'metodo': metodo.pk,
                'detalles': [{'id_menus': menu.pk, 'cantidad': 1}],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertFalse(Venta.objects.exists())
        self.assertFalse(MovimientoCaja.objects.filter(caja=caja).exists())
        self.bebida.refresh_from_db()
        self.assertEqual(self.bebida.stock_actual, Decimal('1.00'))

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


class PedidoOperationalRoleAccessTests(APITestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            usuario='mozo_test',
            email='mozo_test@example.com',
            password='test-password',
        )
        self.rol = Rol.objects.create(nombre='Mozo', estado=True)
        UsuarioRol.objects.create(usuario=self.usuario, rol=self.rol)
        self.local = Local.objects.create(nombre='Sucursal RBAC', direccion='Centro')
        self.empleado = Empleado.objects.create(
            local=self.local,
            usuario=self.usuario,
            dni='11112222',
            nombre='Luis',
            apellido='Mozo',
            telefono='12345678',
            estado=True,
        )
        self.otro_empleado = Empleado.objects.create(
            local=self.local,
            dni='22223333',
            nombre='Otra',
            apellido='Persona',
            telefono='87654321',
            estado=True,
        )
        self.producto = Producto.objects.create(
            nombre='Producto de pedido',
            precio_unitario='10.00',
            estado=True,
        )
        self.bebida = Bebida.objects.create(
            nombre='Bebida de pedido',
            precio_unitario='5.00',
            unidad='unidades',
        )
        self.client.force_authenticate(self.usuario)

    def test_operational_role_can_use_orders_and_required_catalog_reads(self):
        for path in (
            '/api/pedidos/',
            '/api/pedidos/contexto/',
            '/api/productos-listado/',
            '/api/bebidas/',
        ):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200, response.data)

        contexto = self.client.get('/api/pedidos/contexto/')
        self.assertEqual(contexto.data['empleado']['id_empleados'], self.empleado.pk)

    def test_all_operational_roles_can_access_the_orders_module(self):
        for role_name in ('Mozo', 'Cadete', 'Ayudante de cocina', 'Planchero'):
            with self.subTest(role_name=role_name):
                self.rol.nombre = role_name
                self.rol.save(update_fields=['nombre'])
                response = self.client.get('/api/pedidos/')
                self.assertEqual(response.status_code, 200, response.data)

    def test_planchero_and_ayudante_cannot_create_orders(self):
        for role_name in ('Planchero', 'Ayudante', 'Ayudante de cocina'):
            with self.subTest(role_name=role_name):
                self.rol.nombre = role_name
                self.rol.save(update_fields=['nombre'])
                response = self.client.post(
                    '/api/pedidos/',
                    {
                        'empleado': self.empleado.pk,
                        'cliente': 'Cliente restringido',
                        'detalles': [
                            {'id_productos': self.producto.pk, 'cantidad': 1},
                        ],
                    },
                    format='json',
                )
                self.assertEqual(response.status_code, 403, response.data)

    def test_operational_role_cannot_access_sensitive_endpoints_or_catalog_details(self):
        urls = (
            '/api/cajas/',
            '/api/usuarios/',
            '/api/empleados/',
            '/api/compras/',
            '/api/proveedores/',
            '/api/ventas/',
            '/api/dashboard/',
            '/api/productos/',
            f'/api/bebidas/{self.bebida.pk}/',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403, response.data)

        menu_activo = Menu.objects.create(nombre='Menú visible', estado=True)
        menu_inactivo = Menu.objects.create(nombre='Menú oculto', estado=False)
        menus = self.client.get('/api/menus/')
        self.assertEqual(menus.status_code, 200, menus.data)
        menu_results = menus.data.get('results', menus.data)
        self.assertEqual(
            [item['id_menus'] for item in menu_results],
            [menu_activo.pk],
        )
        detalle_menu = self.client.get(f'/api/menus/{menu_activo.pk}/')
        self.assertEqual(detalle_menu.status_code, 403, detalle_menu.data)
        self.assertNotEqual(menu_activo.pk, menu_inactivo.pk)

        bebida_write = self.client.post('/api/bebidas/', {
            'nombre': 'Bebida no autorizada',
            'precio_unitario': '1.00',
        }, format='json')
        self.assertEqual(bebida_write.status_code, 403)

    def test_order_creation_uses_authenticated_operational_employee(self):
        response = self.client.post(
            '/api/pedidos/',
            {
                'empleado': self.otro_empleado.pk,
                'cliente': 'Cliente RBAC',
                'direccion': 'Mesa 1',
                'detalles': [{'id_productos': self.producto.pk, 'cantidad': 1}],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(
            response.data['empleado_detalle']['id_empleados'],
            self.empleado.pk,
        )

    def test_waiter_can_create_order_but_cannot_finalize_it(self):
        intento_finalizado = self.client.post(
            '/api/pedidos/',
            {
                'empleado': self.empleado.pk,
                'cliente': 'Pedido finalizado desde creación',
                'estado': 'Finalizado',
                'detalles': [{'id_productos': self.producto.pk, 'cantidad': 1}],
            },
            format='json',
        )
        self.assertEqual(intento_finalizado.status_code, 403, intento_finalizado.data)

        response = self.client.post(
            '/api/pedidos/',
            {
                'empleado': self.empleado.pk,
                'cliente': 'Cliente Mozo',
                'direccion': 'Mesa 1',
                'detalles': [{'id_productos': self.producto.pk, 'cantidad': 1}],
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201, response.data)

        finalizacion = self.client.patch(
            f"/api/pedidos/{response.data['id_pedidos']}/",
            {'estado': 'Finalizado'},
            format='json',
        )
        self.assertEqual(finalizacion.status_code, 403, finalizacion.data)

    def test_owner_has_full_access_and_operational_user_can_logout(self):
        owner = Usuario.objects.create_user(
            usuario='dueno_test',
            email='dueno_test@example.com',
            password='test-password',
        )
        rol_dueno = Rol.objects.create(nombre='Dueño', estado=True)
        UsuarioRol.objects.create(usuario=owner, rol=rol_dueno)
        self.client.force_authenticate(owner)

        for url in ('/api/cajas/', '/api/usuarios/', '/api/compras/', '/api/proveedores/'):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200, response.data)

        self.client.force_authenticate(self.usuario)
        logout = self.client.post('/api/logout/')
        self.assertEqual(logout.status_code, 200, logout.data)
