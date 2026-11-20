from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from core.models import (
    Caja,
    Compra,
    Local,
    MetodoPago,
    MovimientoCaja,
    Rol,
    Usuario,
    UsuarioRol,
    Venta,
)


class CajaRestriccionesTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            usuario='cajero',
            email='cajero@example.com',
            password='clave',
        )
        self.otro_usuario = Usuario.objects.create_user(
            usuario='otro',
            email='otro@example.com',
            password='clave',
        )
        self.local = Local.objects.create(
            nombre='Local Central',
            direccion='Centro',
        )
        self.rol_admin = Rol.objects.create(nombre='Administrador', estado=True)
        UsuarioRol.objects.create(usuario=self.usuario, rol=self.rol_admin)
        self.token = Token.objects.create(user=self.usuario)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_local_no_puede_tener_dos_cajas_abiertas(self):
        response = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
            'password': 'clave',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        segunda_apertura = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
            'password': 'clave',
        })
        self.assertEqual(segunda_apertura.status_code, status.HTTP_409_CONFLICT)

    def test_apertura_exige_y_revalida_contrasena(self):
        sin_password = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
        })
        incorrecta = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
            'password': 'incorrecta',
        })

        self.assertEqual(sin_password.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(incorrecta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(incorrecta.data['password'], 'La contraseña ingresada es incorrecta.')

    def test_usuario_sin_rol_autorizado_no_puede_abrir_caja(self):
        self.client.force_authenticate(user=self.otro_usuario)
        response = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'],
            'No tiene los permisos adecuados para abrir una caja',
        )

    def test_usuario_no_puede_cerrar_caja_de_otro_usuario(self):
        caja = Caja.objects.create(
            usuario=self.otro_usuario,
            local=self.local,
            monto_apertura=100,
            estado=True,
        )

        response = self.client.patch(f'/api/cajas/{caja.id_cajas}/', {
            'monto_cierre': '90.00',
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listado_indica_si_la_caja_pertenece_al_usuario_autenticado(self):
        caja_propia = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura=100,
            estado=True,
        )
        caja_ajena = Caja.objects.create(
            usuario=self.otro_usuario,
            local=Local.objects.create(nombre='Otra sucursal', direccion='Norte'),
            monto_apertura=100,
            estado=True,
        )

        response = self.client.get('/api/cajas/?status=active')
        cajas = {caja['id_cajas']: caja for caja in response.data}

        self.assertTrue(cajas[caja_propia.id_cajas]['es_mia'])
        self.assertFalse(cajas[caja_ajena.id_cajas]['es_mia'])

    def test_fecha_actual_incluye_cajas_abiertas_de_dias_anteriores(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura=100,
            estado=True,
        )
        Caja.objects.filter(pk=caja.pk).update(
            fecha_hora_apertura=timezone.now() - timedelta(days=1),
        )

        response = self.client.get('/api/cajas/?date=today')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(caja.id_cajas, [item['id_cajas'] for item in response.data])

    def test_historial_filtra_cajas_por_rango_de_fecha_de_apertura(self):
        cajas = []
        for indice in range(3):
            local = Local.objects.create(
                nombre=f'Local historial {indice}',
                direccion=f'Dirección {indice}',
            )
            cajas.append(Caja.objects.create(
                usuario=self.usuario,
                local=local,
                monto_apertura='100.00',
            ))
        ahora = timezone.now()
        fechas = [
            ahora - timedelta(days=2),
            ahora - timedelta(days=1),
            ahora,
        ]
        for caja, fecha in zip(cajas, fechas):
            Caja.objects.filter(pk=caja.pk).update(fecha_hora_apertura=fecha)

        response = self.client.get('/api/cajas/', {
            'fecha_desde': (timezone.localdate() - timedelta(days=1)).isoformat(),
            'fecha_hasta': timezone.localdate().isoformat(),
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {item['id_cajas'] for item in response.data},
            {cajas[1].pk, cajas[2].pk},
        )

    def test_caja_sin_fecha_de_cierre_se_puede_cerrar_aunque_estado_sea_falso(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura=100,
            estado=False,
        )

        listado = self.client.get('/api/cajas/?date=today')
        self.assertIn(caja.id_cajas, [item['id_cajas'] for item in listado.data])

        cierre = self.client.patch(
            f'/api/cajas/{caja.id_cajas}/',
            {
                'confirmar_cierre': True,
                'efectivo_real': '100.00',
                'digital_real': '0.00',
            },
            format='json',
        )

        self.assertEqual(cierre.status_code, status.HTTP_200_OK, cierre.data)
        caja.refresh_from_db()
        self.assertIsNotNone(caja.fecha_hora_cierre)

    def test_no_puede_cerrar_sesion_con_caja_abierta(self):
        Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura=100,
            estado=True,
        )

        response = self.client.post('/api/logout/')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_cierre_calcula_y_guarda_el_saldo_esperado(self):
        efectivo = MetodoPago.objects.create(nombre='Efectivo', estado=True)
        transferencia = MetodoPago.objects.create(nombre='Transferencia QR', estado=True)
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        venta_efectivo = Venta.objects.create(metodo=efectivo, precio_total='25.00')
        MovimientoCaja.objects.create(
            venta=venta_efectivo,
            caja=caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
            concepto='Venta en efectivo',
            monto='25.00',
        )
        compra_efectivo = Compra.objects.create(
            metodo=efectivo,
            precio_total='7.50',
        )
        MovimientoCaja.objects.create(
            compra=compra_efectivo,
            caja=caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO,
            concepto='Compra en efectivo',
            monto='7.50',
        )
        venta_digital = Venta.objects.create(metodo=transferencia, precio_total='30.00')
        MovimientoCaja.objects.create(
            venta=venta_digital,
            caja=caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
            concepto='Venta digital',
            monto='30.00',
        )
        compra_digital = Compra.objects.create(
            metodo=transferencia,
            precio_total='10.00',
        )
        MovimientoCaja.objects.create(
            compra=compra_digital,
            caja=caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO,
            concepto='Compra digital',
            monto='10.00',
        )

        response = self.client.patch(
            f'/api/cajas/{caja.id_cajas}/',
            {
                'confirmar_cierre': True,
                'efectivo_real': '117.50',
                'digital_real': '20.00',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        caja.refresh_from_db()
        self.assertEqual(caja.efectivo_esperado, 117.50)
        self.assertEqual(caja.digital_esperado, 20.00)
        self.assertEqual(caja.efectivo_real, 117.50)
        self.assertEqual(caja.digital_real, 20.00)
        self.assertEqual(caja.diferencia_total, 0)
        self.assertEqual(caja.monto_cierre, 137.50)
        self.assertFalse(caja.estado)
        self.assertIsNotNone(caja.fecha_hora_cierre)
        detalle = self.client.get(f'/api/cajas/{caja.id_cajas}/')
        self.assertEqual(str(detalle.data['efectivo_esperado']), '117.50')
        self.assertEqual(str(detalle.data['digital_esperado']), '20.00')

    def test_cierre_permite_monto_digital_negativo_si_cuadra_con_el_esperado(self):
        transferencia = MetodoPago.objects.create(nombre='Transferencia', estado=True)
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='0.00',
        )
        compra_digital = Compra.objects.create(
            metodo=transferencia,
            precio_total='125600.00',
        )
        MovimientoCaja.objects.create(
            compra=compra_digital,
            caja=caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO,
            concepto='Egreso digital',
            monto='125600.00',
        )

        response = self.client.patch(
            f'/api/cajas/{caja.id_cajas}/',
            {
                'confirmar_cierre': True,
                'efectivo_real': '0.00',
                'digital_real': '-125600.00',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        caja.refresh_from_db()
        self.assertEqual(caja.digital_esperado, -125600)
        self.assertEqual(caja.digital_real, -125600)
        self.assertEqual(caja.diferencia_total, 0)

    def test_saldo_actual_y_movimiento_manual_se_actualizan(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )

        saldo = self.client.get('/api/cajas/?status=active')
        caja_data = next(item for item in saldo.data if item['id_cajas'] == caja.pk)
        self.assertEqual(str(caja_data['saldo_actual']), '100.00')

        ingreso = self.client.post('/api/movimientos-caja/', {
            'caja': caja.pk,
            'tipo_movimiento': 'Ingreso',
            'concepto': 'Ajuste de apertura',
            'monto': '25.00',
        }, format='json')
        self.assertEqual(ingreso.status_code, status.HTTP_201_CREATED, ingreso.data)
        self.assertIsNone(MovimientoCaja.objects.get(pk=ingreso.data['id_movimientos']).venta_id)
        self.assertIsNone(MovimientoCaja.objects.get(pk=ingreso.data['id_movimientos']).compra_id)

        egreso = self.client.post('/api/movimientos-caja/', {
            'caja': caja.pk,
            'tipo_movimiento': 'Egreso',
            'concepto': 'Compra menor',
            'monto': '15.00',
        }, format='json')
        self.assertEqual(egreso.status_code, status.HTTP_201_CREATED, egreso.data)

        caja.refresh_from_db()
        self.assertEqual(caja.saldo_actual, 110)
        detalle = self.client.get('/api/cajas/?status=active')
        caja_data = next(item for item in detalle.data if item['id_cajas'] == caja.pk)
        self.assertEqual(str(caja_data['saldo_actual']), '110.00')

    def test_movimiento_manual_rechaza_egreso_mayor_al_saldo(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='10.00',
        )

        response = self.client.post('/api/movimientos-caja/', {
            'caja': caja.pk,
            'tipo_movimiento': 'Egreso',
            'concepto': 'Egreso excesivo',
            'monto': '10.01',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('saldo insuficiente', response.data['detail'].lower())
        self.assertFalse(MovimientoCaja.objects.filter(caja=caja).exists())

    def test_movimiento_manual_solo_permite_caja_abierta_del_usuario(self):
        caja = Caja.objects.create(
            usuario=self.otro_usuario,
            local=self.local,
            monto_apertura='10.00',
        )
        response = self.client.post('/api/movimientos-caja/', {
            'caja': caja.pk,
            'tipo_movimiento': 'Ingreso',
            'concepto': 'Ingreso ajeno',
            'monto': '1.00',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        caja.usuario = self.usuario
        caja.estado = False
        caja.save(update_fields=['usuario', 'estado'])
        response = self.client.post('/api/movimientos-caja/', {
            'caja': caja.pk,
            'tipo_movimiento': 'Ingreso',
            'concepto': 'Ingreso cerrado',
            'monto': '1.00',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertFalse(MovimientoCaja.objects.filter(caja=caja).exists())

    def test_dashboard_expone_saldo_actual_de_la_caja_activa(self):
        Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='75.00',
        )

        response = self.client.get('/api/dashboard/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['caja_activa']['saldo_actual']), '75.00')

    def test_cierre_con_diferencia_exige_observaciones_de_diez_caracteres(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        payload = {
            'confirmar_cierre': True,
            'efectivo_real': '90.00',
            'digital_real': '0.00',
        }

        sin_observaciones = self.client.patch(
            f'/api/cajas/{caja.id_cajas}/', payload, format='json'
        )
        payload['observaciones_cierre'] = 'Faltante contado'
        con_observaciones = self.client.patch(
            f'/api/cajas/{caja.id_cajas}/', payload, format='json'
        )

        self.assertEqual(sin_observaciones.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(con_observaciones.status_code, status.HTTP_200_OK, con_observaciones.data)
        caja.refresh_from_db()
        self.assertEqual(caja.diferencia_total, -10)
        self.assertEqual(caja.observaciones_cierre, 'Faltante contado')
