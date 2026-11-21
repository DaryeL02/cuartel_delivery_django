from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError

from core.models import Empleado, Local, Rol, Usuario, UsuarioRol
from .serializers import EmpleadoSerializer


class EmpleadoSerializerTests(TestCase):
    def setUp(self):
        local = Local.objects.create(nombre='Local de prueba', direccion='Dirección de prueba')
        self.empleado = Empleado.objects.create(
            local=local,
            dni='12345678',
            nombre='Ana',
            apellido='Pérez',
            telefono='12345678',
            estado=True,
        )

    def test_rejects_duplicate_dni_with_spanish_message(self):
        serializer = EmpleadoSerializer()

        with self.assertRaises(ValidationError) as error:
            serializer.fields['dni'].run_validation('12345678')

        self.assertEqual(
            str(error.exception.detail[0]),
            'Ya existe un empleado registrado con este DNI.',
        )

    def test_allows_employee_to_keep_own_dni(self):
        serializer = EmpleadoSerializer(instance=self.empleado)

        self.assertTrue(serializer.fields['dni'].read_only)

    def test_update_ignores_a_changed_dni(self):
        serializer = EmpleadoSerializer(
            instance=self.empleado,
            data={'dni': '87654321'},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        empleado = serializer.save()
        self.assertEqual(empleado.dni, '12345678')

    def test_empleados_search_matches_employee_name(self):
        usuario = Usuario.objects.create_user(
            usuario='buscador',
            email='buscador@example.com',
            password='clave',
        )
        rol_admin = Rol.objects.create(nombre='Administrador', estado=True)
        UsuarioRol.objects.create(usuario=usuario, rol=rol_admin)
        client = APIClient()
        client.force_authenticate(user=usuario)

        response = client.get('/api/empleados/', {'search': 'Ana'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item['id_empleados'] for item in response.data], [self.empleado.pk])

    def test_create_requires_password(self):
        client = self._admin_client()
        response = client.post('/api/empleados/', self._empleado_payload(), format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)

    def test_password_is_hashed_and_optional_when_updating(self):
        client = self._admin_client()
        payload = self._empleado_payload(password='initial-password')
        response = client.post('/api/empleados/', payload, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        self.assertNotIn('password', response.data['usuario_detalle'])
        empleado = Empleado.objects.get(pk=response.data['id_empleados'])
        usuario = empleado.usuario
        self.assertTrue(usuario.check_password('initial-password'))

        response = client.put(
            f'/api/empleados/{empleado.pk}/',
            {'password': ''},
            format='json',
        )

        self.assertEqual(response.status_code, 200, response.data)
        usuario.refresh_from_db()
        self.assertTrue(usuario.check_password('initial-password'))

        response = client.put(
            f'/api/empleados/{empleado.pk}/',
            {'password': 'updated-password'},
            format='json',
        )

        self.assertEqual(response.status_code, 200, response.data)
        usuario.refresh_from_db()
        self.assertTrue(usuario.check_password('updated-password'))

    def _admin_client(self):
        usuario = Usuario.objects.create_user(
            usuario='admin-empleados',
            email='admin-empleados@example.com',
            password='admin-password',
        )
        rol = Rol.objects.create(nombre='Administrador', estado=True)
        UsuarioRol.objects.create(usuario=usuario, rol=rol)
        client = APIClient()
        client.force_authenticate(user=usuario)
        self.rol_admin = rol
        return client

    def _empleado_payload(self, password=None):
        payload = {
            'rol': self.rol_admin.pk,
            'local': self.empleado.local_id,
            'usuario': 'empleado-nuevo',
            'email': 'empleado-nuevo@example.com',
            'nombre': 'Carlos',
            'apellido': 'Gómez',
            'dni': '87654321',
            'telefono': '12345678',
            'domicilio': 'Calle de prueba',
            'estado': True,
        }
        if password is not None:
            payload['password'] = password
        return payload


class PerfilUsuarioApiTests(TestCase):
    def test_any_authenticated_role_can_update_email_and_hashed_password(self):
        usuario = Usuario.objects.create_user(
            usuario='perfil_planchero',
            email='perfil_planchero@example.com',
            password='old-password',
        )
        rol = Rol.objects.create(nombre='Planchero', estado=True)
        UsuarioRol.objects.create(usuario=usuario, rol=rol)
        client = APIClient()
        client.force_authenticate(user=usuario)

        respuesta = client.get('/api/empleados/me/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['email'], usuario.email)
        self.assertIsNone(respuesta.data['empleado'])
        self.assertNotIn('id_usuarios', respuesta.data)
        self.assertNotIn('usuario', respuesta.data)

        respuesta = client.patch(
            '/api/empleados/me/',
            {
                'email': 'perfil_actualizado@example.com',
                'password': 'new-password',
            },
            format='json',
        )

        self.assertEqual(respuesta.status_code, 200, respuesta.data)
        self.assertEqual(respuesta.data['email'], 'perfil_actualizado@example.com')
        self.assertNotIn('password', respuesta.data)
        usuario.refresh_from_db()
        self.assertEqual(usuario.email, 'perfil_actualizado@example.com')
        self.assertTrue(usuario.check_password('new-password'))
