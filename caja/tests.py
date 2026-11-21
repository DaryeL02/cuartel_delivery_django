from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from core.models import (
    Caja,
    Compra,
    Empleado,
    Local,
    MetodoPago,
    MovimientoCaja,
    Pedido,
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

    def crear_pedido(self, estado, pagado):
        empleado = Empleado.objects.create(
            local=self.local,
            usuario=self.usuario,
            dni='12345678',
            nombre='Cajero',
            apellido='Prueba',
            telefono='12345678',
            estado=True,
        )
        return Pedido.objects.create(
            empleado=empleado,
            cliente='Cliente de prueba',
            direccion='Mesa 1',
            precio_total='10.00',
            estado=estado,
            pagado=pagado,
        )

    def datos_cierre(self):
        return {
            'confirmar_cierre': True,
            'efectivo_real': '100.00',
            'digital_real': '0.00',
            'password': 'clave',
        }

    def test_local_no_puede_tener_dos_cajas_abiertas(self):
        response = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
            'password': 'clave',
            'justificacion_apertura': 'Fondo inicial',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['ajuste_apertura'], '50.00')
        self.assertEqual(
            MovimientoCaja.objects.get(caja_id=response.data['id_cajas']).tipo_movimiento,
            MovimientoCaja.TipoMovimiento.INGRESO,
        )

        segunda_apertura = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
            'password': 'clave',
            'justificacion_apertura': 'Fondo inicial',
        })
        self.assertEqual(segunda_apertura.status_code, status.HTTP_409_CONFLICT)

    def test_apertura_expone_el_ajuste_negativo(self):
        anterior = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
            efectivo_real='100.00',
            estado=False,
            fecha_hora_cierre=timezone.now() - timedelta(hours=1),
        )
        response = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '85.00',
            'password': 'clave',
            'justificacion_apertura': 'Menos efectivo inicial',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['ajuste_apertura'], '-15.00')
        caja = Caja.objects.get(pk=response.data['id_cajas'])
        self.assertEqual(caja.ajuste_apertura, -15)
        movimiento = MovimientoCaja.objects.get(caja=caja)
        self.assertEqual(movimiento.tipo_movimiento, MovimientoCaja.TipoMovimiento.EGRESO)
        detalle = self.client.get(f'/api/cajas/{caja.pk}/')
        self.assertEqual(detalle.data['ajuste_apertura'], '-15.00')

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
                'password': 'clave',
            },
            format='json',
        )

        self.assertEqual(cierre.status_code, status.HTTP_200_OK, cierre.data)
        caja.refresh_from_db()
        self.assertIsNotNone(caja.fecha_hora_cierre)

    def test_cierre_bloquea_pedidos_en_proceso_aunque_esten_pagados(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        self.crear_pedido(Pedido.Estado.EN_PROCESO, pagado=True)

        cierre = self.client.patch(
            f'/api/cajas/{caja.pk}/',
            self.datos_cierre(),
            format='json',
        )

        self.assertEqual(cierre.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('1 pedido en proceso', cierre.data['detail'])
        self.assertNotIn('sin pagar', cierre.data['detail'])
        caja.refresh_from_db()
        self.assertIsNone(caja.fecha_hora_cierre)

    def test_cierre_bloquea_pedido_finalizado_pendiente_de_pago(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        self.crear_pedido(Pedido.Estado.FINALIZADO, pagado=False)

        cierre = self.client.patch(
            f'/api/cajas/{caja.pk}/',
            self.datos_cierre(),
            format='json',
        )

        self.assertEqual(cierre.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('1 pedido no cancelado sin pagar', cierre.data['detail'])

    def test_pedido_cancelado_impago_no_bloquea_cierre(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        self.crear_pedido(Pedido.Estado.CANCELADO, pagado=False)

        cierre = self.client.patch(
            f'/api/cajas/{caja.pk}/',
            self.datos_cierre(),
            format='json',
        )

        self.assertEqual(cierre.status_code, status.HTTP_200_OK, cierre.data)

    def test_pedido_impago_de_otro_local_no_bloquea_el_cierre(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        otro_local = Local.objects.create(nombre='Otra sucursal', direccion='Norte')
        empleado_ajeno = Empleado.objects.create(
            local=otro_local,
            usuario=self.otro_usuario,
            dni='87654321',
            nombre='Otro',
            apellido='Empleado',
            telefono='87654321',
            estado=True,
        )
        Pedido.objects.create(
            empleado=empleado_ajeno,
            cliente='Cliente de otra sucursal',
            direccion='Mesa 2',
            precio_total='10.00',
            estado=Pedido.Estado.FINALIZADO,
            pagado=False,
        )

        cierre = self.client.patch(
            f'/api/cajas/{caja.pk}/',
            self.datos_cierre(),
            format='json',
        )

        self.assertEqual(cierre.status_code, status.HTTP_200_OK, cierre.data)

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
                'password': 'clave',
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

    def test_cierre_anterior_expone_efectivo_final_para_comparar_apertura(self):
        anterior = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
            efectivo_esperado='115.00',
            efectivo_real='120.00',
            digital_esperado='10.00',
            digital_real='10.00',
            monto_cierre='130.00',
            estado=False,
            fecha_hora_cierre=timezone.now() - timedelta(hours=1),
        )
        anterior.fecha_hora_apertura = timezone.now() - timedelta(days=1)
        anterior.save(update_fields=['fecha_hora_apertura'])
        nueva = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='125.00',
        )

        respuesta = self.client.get('/api/cajas/')
        datos_nueva = next(item for item in respuesta.data if item['id_cajas'] == nueva.pk)

        self.assertEqual(str(datos_nueva['efectivo_cierre_anterior']), '120.00')

    def test_historial_para_apertura_filtra_por_local_y_solo_cajas_cerradas(self):
        anterior = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
            efectivo_real='80.00',
            estado=False,
            fecha_hora_cierre=timezone.now() - timedelta(hours=1),
        )
        Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='999.00',
            estado=True,
        )
        otro_local = Local.objects.create(nombre='Sucursal ajena', direccion='Sur')
        Caja.objects.create(
            usuario=self.usuario,
            local=otro_local,
            monto_apertura='500.00',
            efectivo_real='450.00',
            estado=False,
            fecha_hora_cierre=timezone.now(),
        )

        respuesta = self.client.get('/api/cajas/', {
            'local': self.local.pk,
            'solo_cerradas': 'true',
        })

        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual([item['id_cajas'] for item in respuesta.data], [anterior.pk])
        self.assertEqual(str(respuesta.data[0]['efectivo_real']), '80.00')

    def test_movimiento_manual_digital_se_refleja_en_el_arqueo_digital(self):
        transferencia = MetodoPago.objects.create(nombre='Transferencia QR', estado=True)
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )

        response = self.client.post('/api/movimientos-caja/', {
            'caja': caja.pk,
            'metodo': transferencia.pk,
            'tipo_movimiento': 'Ingreso',
            'concepto': 'Transferencia manual',
            'monto': '25.00',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['metodo_detalle'], transferencia.nombre)
        caja_data = self.client.get(f'/api/cajas/{caja.pk}/').data
        self.assertEqual(str(caja_data['efectivo_esperado']), '100.00')
        self.assertEqual(str(caja_data['digital_esperado']), '25.00')

    def test_egreso_digital_no_puede_usar_saldo_en_efectivo(self):
        transferencia = MetodoPago.objects.create(nombre='Transferencia QR', estado=True)
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )

        respuesta = self.client.post('/api/movimientos-caja/', {
            'caja': caja.pk,
            'metodo': transferencia.pk,
            'tipo_movimiento': 'Egreso',
            'concepto': 'Egreso digital',
            'monto': '1.00',
        }, format='json')

        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Saldo insuficiente', respuesta.data['detail'])
        self.assertFalse(MovimientoCaja.objects.filter(caja=caja).exists())

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
                'password': 'clave',
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
        self.assertEqual(str(caja_data['efectivo_esperado']), '110.00')
        self.assertEqual(str(caja_data['digital_esperado']), '0.00')

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
            'password': 'clave',
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

    def test_apertura_diferente_exige_justificacion_y_crea_ajuste(self):
        anterior = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
            efectivo_real='80.00',
            estado=False,
            fecha_hora_cierre=timezone.now() - timedelta(minutes=1),
        )

        sin_justificacion = self.client.post('/api/cajas/', {
            'local': self.local.pk,
            'monto_apertura': '75.00',
            'password': 'clave',
        }, format='json')
        self.assertEqual(sin_justificacion.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('justificacion_apertura', sin_justificacion.data)
        self.assertFalse(Caja.objects.filter(local=self.local, pk__gt=anterior.pk).exists())

        apertura = self.client.post('/api/cajas/', {
            'local': self.local.pk,
            'monto_apertura': '75.00',
            'password': 'clave',
            'justificacion_apertura': 'Faltante detectado',
        }, format='json')

        self.assertEqual(apertura.status_code, status.HTTP_201_CREATED, apertura.data)
        movimiento = MovimientoCaja.objects.get(caja_id=apertura.data['id_cajas'])
        self.assertEqual(movimiento.tipo_movimiento, MovimientoCaja.TipoMovimiento.EGRESO)
        self.assertEqual(movimiento.concepto, 'Faltante detectado')
        self.assertEqual(movimiento.monto, 5)
        caja_abierta = Caja.objects.get(pk=apertura.data['id_cajas'])
        self.assertEqual(caja_abierta.monto_apertura, 80)
        self.assertEqual(caja_abierta.saldo_actual, 75)
        self.assertIsNone(movimiento.venta_id)
        self.assertIsNone(movimiento.compra_id)

    def test_apertura_sin_diferencia_no_exige_justificacion_ni_crea_ajuste(self):
        Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
            efectivo_real='80.00',
            estado=False,
            fecha_hora_cierre=timezone.now() - timedelta(minutes=1),
        )

        apertura = self.client.post('/api/cajas/', {
            'local': self.local.pk,
            'monto_apertura': '80.00',
            'password': 'clave',
        }, format='json')

        self.assertEqual(apertura.status_code, status.HTTP_201_CREATED, apertura.data)
        self.assertFalse(
            MovimientoCaja.objects.filter(caja_id=apertura.data['id_cajas']).exists()
        )

    def test_apertura_superior_al_cierre_crea_ingreso_por_la_diferencia(self):
        Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
            efectivo_real='80.00',
            estado=False,
            fecha_hora_cierre=timezone.now() - timedelta(minutes=1),
        )

        apertura = self.client.post('/api/cajas/', {
            'local': self.local.pk,
            'monto_apertura': '85.00',
            'password': 'clave',
            'justificacion_apertura': 'Reposición de efectivo',
        }, format='json')

        self.assertEqual(apertura.status_code, status.HTTP_201_CREATED, apertura.data)
        movimiento = MovimientoCaja.objects.get(caja_id=apertura.data['id_cajas'])
        self.assertEqual(movimiento.tipo_movimiento, MovimientoCaja.TipoMovimiento.INGRESO)
        self.assertEqual(movimiento.monto, 5)

    def test_sin_cierre_previo_el_base_es_cero_y_el_ingreso_cuadra_con_el_monto(self):
        sin_justificacion = self.client.post('/api/cajas/', {
            'local': self.local.pk,
            'monto_apertura': '90.00',
            'password': 'clave',
        }, format='json')
        self.assertEqual(sin_justificacion.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('justificacion_apertura', sin_justificacion.data)
        self.assertFalse(Caja.objects.filter(local=self.local).exists())

        apertura = self.client.post('/api/cajas/', {
            'local': self.local.pk,
            'monto_apertura': '90.00',
            'password': 'clave',
            'justificacion_apertura': 'Fondo inicial',
        }, format='json')

        self.assertEqual(apertura.status_code, status.HTTP_201_CREATED, apertura.data)
        caja = Caja.objects.get(pk=apertura.data['id_cajas'])
        movimiento = MovimientoCaja.objects.get(caja=caja)
        self.assertEqual(caja.monto_apertura, 0)
        self.assertEqual(movimiento.tipo_movimiento, MovimientoCaja.TipoMovimiento.INGRESO)
        self.assertEqual(movimiento.monto, 90)
        self.assertEqual(caja.saldo_actual, 90)

    def test_cierre_exige_password_correcto(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        datos = {
            'confirmar_cierre': True,
            'efectivo_real': '100.00',
            'digital_real': '0.00',
        }

        sin_password = self.client.patch(
            f'/api/cajas/{caja.pk}/', datos, format='json'
        )
        datos['password'] = 'incorrecta'
        password_incorrecto = self.client.patch(
            f'/api/cajas/{caja.pk}/', datos, format='json'
        )
        caja.refresh_from_db()

        self.assertEqual(sin_password.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', sin_password.data)
        self.assertEqual(password_incorrecto.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            password_incorrecto.data['password'],
            'La contraseña ingresada es incorrecta.',
        )
        self.assertTrue(caja.estado)
        self.assertIsNone(caja.fecha_hora_cierre)

    def test_edicion_actualiza_solo_movimiento_manual_y_saldo(self):
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        movimiento = MovimientoCaja.objects.create(
            caja=caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
            concepto='Ingreso manual',
            monto='20.00',
        )

        actualizado = self.client.patch(
            f'/api/movimientos-caja/{movimiento.pk}/',
            {
                'tipo_movimiento': 'Egreso',
                'concepto': 'Gasto manual',
                'monto': '15.00',
            },
            format='json',
        )

        self.assertEqual(actualizado.status_code, status.HTTP_200_OK, actualizado.data)
        movimiento.refresh_from_db()
        self.assertEqual(movimiento.tipo_movimiento, MovimientoCaja.TipoMovimiento.EGRESO)
        self.assertEqual(movimiento.concepto, 'Gasto manual')
        self.assertEqual(movimiento.monto, 15)
        caja.refresh_from_db()
        self.assertEqual(caja.saldo_actual, 85)

    def test_edicion_rechaza_movimientos_vinculados_a_venta_o_compra(self):
        efectivo = MetodoPago.objects.create(nombre='Efectivo', estado=True)
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        venta = Venta.objects.create(metodo=efectivo, precio_total='10.00')
        compra = Compra.objects.create(metodo=efectivo, precio_total='5.00')
        movimientos = (
            MovimientoCaja.objects.create(
                caja=caja,
                venta=venta,
                tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
                concepto='Venta',
                monto='10.00',
            ),
            MovimientoCaja.objects.create(
                caja=caja,
                compra=compra,
                tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO,
                concepto='Compra',
                monto='5.00',
            ),
        )

        for movimiento in movimientos:
            response = self.client.patch(
                f'/api/movimientos-caja/{movimiento.pk}/',
                {'concepto': 'Intento de edición'},
                format='json',
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.data['detail'],
                'Solo se pueden editar movimientos manuales.',
            )
