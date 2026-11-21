from django.test import TestCase
from rest_framework.test import APITestCase
from django.utils import timezone
from .serializers import BebidaSerializer, InsumoSerializer, ProveedorSerializer
from core.models import (
    Bebida,
    Caja,
    Categoria,
    Compra,
    Insumo,
    Local,
    MetodoPago,
    MovimientoCaja,
    Proveedor,
    Rol,
    Usuario,
    UsuarioRol,
)


class ProveedorSerializerTests(TestCase):
    def test_only_name_is_required(self):
        serializer = ProveedorSerializer(data={'nombre': 'Proveedor de prueba'})

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_rejects_non_numeric_phone_and_tax_id(self):
        serializer = ProveedorSerializer(data={
            'nombre': 'Proveedor inválido',
            'telefono': '123-abc',
            'cuit': '20-12345678-9',
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('telefono', serializer.errors)
        self.assertIn('cuit', serializer.errors)


class CatalogNameValidationTests(TestCase):
    def test_insumo_names_are_unique_case_insensitively(self):
        categoria = Categoria.objects.create(nombre='Almacén')
        Insumo.objects.create(
            categoria=categoria,
            nombre='Harina',
            unidad='kg',
            stock_actual=1,
            stock_minimo=0,
        )
        serializer = InsumoSerializer(data={
            'categoria': categoria.pk,
            'nombre': 'HARINA',
            'unidad': 'kg',
            'stock_actual': 0,
            'stock_minimo': 0,
        })

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['nombre'][0]),
            'Ya existe un registro con este nombre',
        )

    def test_beverage_serializer_defaults_unit(self):
        serializer = BebidaSerializer(data={
            'nombre': 'Agua sin gas',
            'precio_unitario': '10.00',
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)
        bebida = serializer.save()
        self.assertEqual(bebida.unidad, 'unidades')

    def test_beverage_names_are_unique_case_insensitively(self):
        Bebida.objects.create(
            nombre='Agua',
            precio_unitario='10.00',
            unidad='unidades',
        )
        serializer = BebidaSerializer(data={
            'nombre': 'AGUA',
            'precio_unitario': '11.00',
        })

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['nombre'][0]),
            'Ya existe un registro con este nombre',
        )


class CompraApiTests(APITestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            usuario='comprador_test',
            email='comprador_test@example.com',
            password='test-password',
        )
        rol_admin = Rol.objects.create(nombre='Administrador', estado=True)
        UsuarioRol.objects.create(usuario=self.usuario, rol=rol_admin)
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

    def test_purchase_requires_open_cash_register(self):
        self.caja.delete()

        response = self.client.post('/api/compras/', {
            'proveedor': self.proveedor.pk,
            'metodo': self.metodo.pk,
            'detalles': [
                {'insumo': self.insumo.pk, 'cantidad': 1, 'precio_unitario': '2.50'},
            ],
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('caja abierta', str(response.data).lower())
        self.assertEqual(Compra.objects.count(), 0)
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.stock_actual, 4)

    def test_purchase_rejects_amount_above_cash_balance_without_side_effects(self):
        self.caja.monto_apertura = '5.00'
        self.caja.save(update_fields=['monto_apertura'])

        response = self.client.post('/api/compras/', {
            'proveedor': self.proveedor.pk,
            'metodo': self.metodo.pk,
            'detalles': [
                {'insumo': self.insumo.pk, 'cantidad': 3, 'precio_unitario': '2.50'},
            ],
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('saldo insuficiente', str(response.data).lower())
        self.assertEqual(Compra.objects.count(), 0)
        self.assertFalse(MovimientoCaja.objects.exists())
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.stock_actual, 4)

    def test_digital_purchase_is_allowed_when_cash_balance_is_lower(self):
        self.caja.monto_apertura = '5.00'
        self.caja.save(update_fields=['monto_apertura'])
        transferencia = MetodoPago.objects.create(
            nombre='Transferencia QR',
            estado=True,
        )

        response = self.client.post('/api/compras/', {
            'proveedor': self.proveedor.pk,
            'metodo_efectivo': self.metodo.pk,
            'metodo_transferencia': transferencia.pk,
            'monto_efectivo': '0.00',
            'monto_transferencia': '7.50',
            'detalles': [
                {'insumo': self.insumo.pk, 'cantidad': 3, 'precio_unitario': '2.50'},
            ],
        }, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        movimiento = MovimientoCaja.objects.get(compra_id=response.data['id_compras'])
        self.assertEqual(movimiento.metodo, transferencia)
        esperado_efectivo, esperado_digital = self.caja.montos_esperados()
        self.assertEqual(str(esperado_efectivo), '5.00')
        self.assertEqual(str(esperado_digital), '-7.50')

    def test_purchase_can_be_paid_entirely_in_cash(self):
        response = self.client.post('/api/compras/', {
            'metodo_efectivo': self.metodo.pk,
            'metodo_transferencia': MetodoPago.objects.create(
                nombre='Transferencia QR',
                estado=True,
            ).pk,
            'monto_efectivo': '5.00',
            'monto_transferencia': '0.00',
            'detalles': [
                {'insumo': self.insumo.pk, 'cantidad': 2, 'precio_unitario': '2.50'},
            ],
        }, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Compra.objects.count(), 1)
        self.assertEqual(response.data['metodo'], self.metodo.pk)
        self.assertEqual(len(response.data['detalle_compra']), 1)
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.stock_actual, 6)

    def test_purchase_splits_details_by_payment_method_without_supplier(self):
        self.caja.monto_apertura = '5.00'
        self.caja.save(update_fields=['monto_apertura'])
        transferencia = MetodoPago.objects.create(
            nombre='Transferencia QR',
            estado=True,
        )

        response = self.client.post('/api/compras/', {
            'proveedor': None,
            'metodo_efectivo': self.metodo.pk,
            'metodo_transferencia': transferencia.pk,
            'monto_efectivo': '5.00',
            'monto_transferencia': '8.00',
            'detalles': [
                {
                    'insumo': self.insumo.pk,
                    'cantidad': 2,
                    'precio_unitario': '2.50',
                },
                {
                    'bebida': self.bebida.pk,
                    'cantidad': 2,
                    'precio_unitario': '4.00',
                },
            ],
        }, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        compras = response.data['compras']
        self.assertEqual(len(compras), 2)
        por_metodo = {item['metodo']: item for item in compras}
        self.assertEqual(por_metodo[self.metodo.pk]['precio_total'], '5.00')
        self.assertEqual(por_metodo[transferencia.pk]['precio_total'], '8.00')
        self.assertEqual(len(por_metodo[self.metodo.pk]['detalle_compra']), 2)
        self.assertEqual(por_metodo[transferencia.pk]['detalle_compra'], [])
        self.assertEqual(
            {
                item['insumo']['id_insumos']
                for item in por_metodo[self.metodo.pk]['detalle_compra']
                if item['insumo']
            },
            {self.insumo.pk},
        )
        self.assertEqual(
            {
                item['bebida']['id_bebidas']
                for item in por_metodo[self.metodo.pk]['detalle_compra']
                if item['bebida']
            },
            {self.bebida.pk},
        )
        self.assertEqual(Compra.objects.filter(proveedor__isnull=True).count(), 2)

        self.insumo.refresh_from_db()
        self.bebida.refresh_from_db()
        self.assertEqual(self.insumo.stock_actual, 6)
        self.assertEqual(self.bebida.stock_actual, 2)
        movimientos = MovimientoCaja.objects.filter(compra__in=Compra.objects.all())
        self.assertEqual(movimientos.count(), 2)
        self.assertEqual(
            set(movimientos.values_list('metodo_id', flat=True)),
            {self.metodo.pk, transferencia.pk},
        )

    def test_split_purchase_requires_payment_total_to_match_details(self):
        transferencia = MetodoPago.objects.create(
            nombre='Transferencia QR',
            estado=True,
        )

        response = self.client.post('/api/compras/', {
            'metodo_efectivo': self.metodo.pk,
            'metodo_transferencia': transferencia.pk,
            'monto_efectivo': '5.00',
            'monto_transferencia': '7.99',
            'detalles': [
                {'insumo': self.insumo.pk, 'cantidad': 2, 'precio_unitario': '2.50'},
                {'bebida': self.bebida.pk, 'cantidad': 2, 'precio_unitario': '4.00'},
            ],
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('suma de los pagos', str(response.data).lower())
        self.assertEqual(Compra.objects.count(), 0)
        self.assertFalse(MovimientoCaja.objects.exists())
        self.insumo.refresh_from_db()
        self.bebida.refresh_from_db()
        self.assertEqual(self.insumo.stock_actual, 4)
        self.assertEqual(self.bebida.stock_actual, 0)

    def test_split_purchase_rejects_cash_amount_above_cash_balance(self):
        self.caja.monto_apertura = '5.00'
        self.caja.save(update_fields=['monto_apertura'])
        transferencia = MetodoPago.objects.create(
            nombre='Transferencia QR',
            estado=True,
        )

        response = self.client.post('/api/compras/', {
            'metodo_efectivo': self.metodo.pk,
            'metodo_transferencia': transferencia.pk,
            'monto_efectivo': '5.01',
            'monto_transferencia': '2.49',
            'detalles': [
                {'insumo': self.insumo.pk, 'cantidad': 3, 'precio_unitario': '2.50'},
            ],
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('saldo insuficiente', str(response.data).lower())
        self.assertEqual(Compra.objects.count(), 0)
        self.assertFalse(MovimientoCaja.objects.exists())
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.stock_actual, 4)

    def test_purchase_history_filters_and_paginates_twenty_records(self):
        compras = []
        for indice in range(21):
            compra = Compra.objects.create(
                metodo=self.metodo,
                proveedor=self.proveedor,
                precio_total='1.00',
            )
            compras.append(compra)
            MovimientoCaja.objects.create(
                compra=compra,
                caja=self.caja,
                tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO,
                concepto=f'Compra #{compra.pk}',
                monto='1.00',
            )

        MovimientoCaja.objects.create(
            compra=compras[0],
            caja=self.caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO,
            concepto=f'Compra #{compras[0].pk} repetida',
            monto='1.00',
        )
        hoy = timezone.localdate().isoformat()
        filtros = {
            'fecha_desde': hoy,
            'fecha_hasta': hoy,
            'proveedor': self.proveedor.pk,
            'id_cajas': self.caja.pk,
        }

        primera_pagina = self.client.get('/api/compras/', filtros)
        filtros['page'] = 2
        segunda_pagina = self.client.get('/api/compras/', filtros)

        self.assertEqual(primera_pagina.data['count'], 21)
        self.assertEqual(len(primera_pagina.data['results']), 20)
        self.assertEqual(len(segunda_pagina.data['results']), 1)
