from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from core.models import Caja, Local, MovimientoCaja, Rol, Usuario, UsuarioRol


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
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        segunda_apertura = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
        })
        self.assertEqual(segunda_apertura.status_code, status.HTTP_409_CONFLICT)

    def test_usuario_sin_rol_autorizado_no_puede_abrir_caja(self):
        self.client.force_authenticate(user=self.otro_usuario)
        response = self.client.post('/api/cajas/', {
            'local': self.local.id_locales,
            'monto_apertura': '50.00',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        caja = Caja.objects.create(
            usuario=self.usuario,
            local=self.local,
            monto_apertura='100.00',
        )
        MovimientoCaja.objects.create(
            caja=caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
            concepto='Ingreso test',
            monto='25.00',
        )
        MovimientoCaja.objects.create(
            caja=caja,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.EGRESO,
            concepto='Egreso test',
            monto='7.50',
        )

        response = self.client.patch(
            f'/api/cajas/{caja.id_cajas}/',
            {'confirmar_cierre': True},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        caja.refresh_from_db()
        self.assertEqual(caja.monto_cierre, 117.50)
        self.assertFalse(caja.estado)
        self.assertIsNotNone(caja.fecha_hora_cierre)
