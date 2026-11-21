from rest_framework.test import APITestCase

from core.models import Bebida, Menu, Producto, Rol, Usuario, UsuarioRol


class MenuBebidaApiTests(APITestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            usuario='menu_admin',
            email='menu_admin@example.com',
            password='test-password',
        )
        rol = Rol.objects.create(nombre='Administrador', estado=True)
        UsuarioRol.objects.create(usuario=self.usuario, rol=rol)
        self.producto = Producto.objects.create(
            nombre='Hamburguesa menú',
            precio_unitario='10.00',
            estado=True,
        )
        self.bebida = Bebida.objects.create(
            nombre='Agua menú',
            precio_unitario='3.00',
            unidad='unidades',
        )
        self.client.force_authenticate(self.usuario)

    def test_menu_creates_and_updates_product_and_beverage_details(self):
        response = self.client.post('/api/menus/', {
            'nombre': 'Menú completo',
            'estado': True,
            'detalles': [
                {
                    'producto': self.producto.pk,
                    'bebida': None,
                    'cantidad': 1,
                    'descuento': 0,
                },
                {
                    'producto': None,
                    'bebida': self.bebida.pk,
                    'cantidad': 2,
                    'descuento': 5,
                },
            ],
        }, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        detalle_bebida = next(
            detalle for detalle in response.data['detalles'] if detalle['bebida']
        )
        self.assertEqual(detalle_bebida['bebida_data']['nombre'], self.bebida.nombre)
        self.assertEqual(Menu.objects.get(pk=response.data['id_menus']).detalles.count(), 2)

        response = self.client.patch(
            f"/api/menus/{response.data['id_menus']}/",
            {
                'detalles': [{
                    'producto': None,
                    'bebida': self.bebida.pk,
                    'cantidad': 3,
                    'descuento': 0,
                }],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['detalles'][0]['bebida'], self.bebida.pk)
        self.assertEqual(response.data['detalles'][0]['cantidad'], 3)
