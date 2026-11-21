import re

from django.core import mail
from django.test import override_settings
from rest_framework.test import APITestCase

from core.models import (
	Categoria,
	DetalleCompra,
	DetalleMenu,
	Insumo,
	Menu,
	MetodoPago,
	Producto,
	Proveedor,
	ProveedorInsumo,
	Rol,
	Usuario,
	UsuarioRol,
)
from rest_framework.authtoken.models import Token


@override_settings(
	EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
	FRONTEND_URL='http://localhost:3000',
)
class PasswordResetApiTests(APITestCase):
	def setUp(self):
		self.user = Usuario.objects.create_user(
			usuario='prueba',
			email='prueba@example.com',
			password='Original-Password-548!',
		)

	def test_request_sends_reset_link_without_disclosing_unknown_email(self):
		response = self.client.post(
			'/api/password-reset/', {'email': self.user.email}, format='json'
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(mail.outbox), 1)
		self.assertIn('recibirás instrucciones', response.data['detail'].lower())
		self.assertIn('reset-password?uid=', mail.outbox[0].body)

		unknown_response = self.client.post(
			'/api/password-reset/', {'email': 'unknown@example.com'}, format='json'
		)
		self.assertEqual(unknown_response.status_code, 200)
		self.assertEqual(unknown_response.data, response.data)
		self.assertEqual(len(mail.outbox), 1)

	def test_valid_link_changes_password_and_revokes_old_token(self):
		old_token = Token.objects.create(user=self.user)
		self.client.post(
			'/api/password-reset/', {'email': self.user.email}, format='json'
		)
		match = re.search(r'uid=([^&\s]+)&token=([^\s]+)', mail.outbox[0].body)
		self.assertIsNotNone(match)

		response = self.client.post(
			'/api/password-reset/confirm/',
			{
				'uid': match.group(1),
				'token': match.group(2),
				'new_password': 'New-Password-938!Secure',
			},
			format='json',
		)

		self.assertEqual(response.status_code, 200)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('New-Password-938!Secure'))
		self.assertFalse(Token.objects.filter(key=old_token.key).exists())

	def test_invalid_token_does_not_change_password(self):
		response = self.client.post(
			'/api/password-reset/confirm/',
			{
				'uid': 'MQ',
				'token': 'invalid-token',
				'new_password': 'New-Password-938!Secure',
			},
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('Original-Password-548!'))


class CompraApiTests(APITestCase):
	def setUp(self):
		self.user = Usuario.objects.create_user(
			usuario='compras-admin',
			password='Password-548!',
			is_staff=True,
		)
		self.client.force_authenticate(user=self.user)
		self.metodo = MetodoPago.objects.create(
			nombre='Transferencia',
			descripcion='Pago bancario',
			estado=True,
		)
		self.proveedor = Proveedor.objects.create(
			nombre='Distribuidora Central',
			email='ventas@example.com',
		)
		self.categoria = Categoria.objects.create(
			nombre='Insumos',
			descripcion='Insumos generales',
		)
		self.insumo = Insumo.objects.create(
			categoria=self.categoria,
			nombre='Harina',
			unidad='kg',
			stock_actual=10,
			stock_minimo=5,
		)
		ProveedorInsumo.objects.create(
			proveedor=self.proveedor,
			insumo=self.insumo,
		)

	def test_create_purchase_updates_supplier_and_stock(self):
		response = self.client.post(
			'/api/compras/',
			{
				'metodo': self.metodo.pk,
				'proveedor': self.proveedor.pk,
				'detalles': [
					{
						'insumo': self.insumo.pk,
						'cantidad': 25,
						'subtotal': '12500.00',
					}
				],
			},
			format='json',
		)

		self.assertEqual(response.status_code, 201, response.data)
		self.assertEqual(str(response.data['precio_total']), '12500.00')
		self.insumo.refresh_from_db()
		self.assertEqual(self.insumo.stock_actual, 35)
		self.assertEqual(DetalleCompra.objects.count(), 1)

	def test_create_purchase_with_cash_and_transfer_payments(self):
		response = self.client.post(
			'/api/compras/',
			{
				'proveedor': self.proveedor.pk,
				'monto_efectivo': '4000.00',
				'monto_transferencia': '8500.00',
				'detalles': [
					{
						'insumo': self.insumo.pk,
						'cantidad': 1,
						'subtotal': '12500.00',
					}
				],
			},
			format='json',
		)

		self.assertEqual(response.status_code, 201, response.data)
		self.assertEqual(str(response.data['monto_efectivo']), '4000.00')
		self.assertEqual(str(response.data['monto_transferencia']), '8500.00')

	def test_rejects_payment_sum_above_purchase_total(self):
		response = self.client.post(
			'/api/compras/',
			{
				'proveedor': self.proveedor.pk,
				'monto_efectivo': '10000.00',
				'monto_transferencia': '2500.01',
				'detalles': [
					{
						'insumo': self.insumo.pk,
						'cantidad': 1,
						'subtotal': '12500.00',
					}
				],
			},
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.insumo.refresh_from_db()
		self.assertEqual(self.insumo.stock_actual, 10)
		self.assertEqual(DetalleCompra.objects.count(), 0)

	def test_rejects_insumo_not_supplied_by_provider(self):
		otro_insumo = Insumo.objects.create(
			categoria=self.categoria,
			nombre='Azucar',
			unidad='kg',
			stock_actual=10,
			stock_minimo=5,
		)

		response = self.client.post(
			'/api/compras/',
			{
				'metodo': self.metodo.pk,
				'proveedor': self.proveedor.pk,
				'detalles': [
					{
						'insumo': otro_insumo.pk,
						'cantidad': 10,
						'subtotal': '1000.00',
					}
				],
			},
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn('detalles', response.data)


class MenuApiTests(APITestCase):
	def setUp(self):
		self.user = Usuario.objects.create_user(
			usuario='menu-user',
			password='Password-548!',
			is_staff=True,
		)
		self.client.force_authenticate(user=self.user)
		self.producto = Producto.objects.create(
			nombre='Hamburguesa',
			precio_unitario='2500.00',
			estado=True,
		)

	def test_create_menu_with_product_details(self):
		response = self.client.post(
			'/api/menus/',
			{
				'nombre': 'Menú del día',
				'estado': True,
				'detalles': [
					{
						'producto': self.producto.pk,
						'cantidad': 2,
						'descuento': 100,
					}
				],
			},
			format='json',
		)

		self.assertEqual(response.status_code, 201, response.data)
		self.assertEqual(response.data['nombre'], 'Menú del día')
		self.assertEqual(response.data['detalles'][0]['producto_data']['nombre'], 'Hamburguesa')
		self.assertEqual(DetalleMenu.objects.count(), 1)

	def test_update_menu_replaces_details_and_delete_cascades(self):
		menu = Menu.objects.create(nombre='Menú anterior', estado=True)
		DetalleMenu.objects.create(
			menu=menu,
			producto=self.producto,
			cantidad=1,
			descuento=0,
		)

		response = self.client.patch(
			f'/api/menus/{menu.pk}/',
			{'detalles': []},
			format='json',
		)
		self.assertEqual(response.status_code, 200, response.data)
		self.assertEqual(DetalleMenu.objects.filter(menu=menu).count(), 0)

		DetalleMenu.objects.create(
			menu=menu,
			producto=self.producto,
			cantidad=1,
			descuento=0,
		)
		response = self.client.delete(f'/api/menus/{menu.pk}/')
		self.assertEqual(response.status_code, 204)
		self.assertFalse(Menu.objects.filter(pk=menu.pk).exists())
		self.assertEqual(DetalleMenu.objects.count(), 0)

	def test_menu_rejects_duplicate_products(self):
		response = self.client.post(
			'/api/menus/',
			{
				'nombre': 'Menú duplicado',
				'estado': True,
				'detalles': [
					{'producto': self.producto.pk, 'cantidad': 1, 'descuento': 0},
					{'producto': self.producto.pk, 'cantidad': 2, 'descuento': 0},
				],
			},
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(Menu.objects.count(), 0)

	def test_non_admin_can_view_menus_but_cannot_modify_them(self):
		menu = Menu.objects.create(nombre='Menú existente', estado=True)
		regular_user = Usuario.objects.create_user(
			usuario='regular-user',
			password='Password-548!',
		)
		self.client.force_authenticate(user=regular_user)

		self.assertEqual(self.client.get('/api/menus/').status_code, 200)
		self.assertEqual(
			self.client.post(
				'/api/menus/',
				{'nombre': 'Menú no autorizado', 'estado': True},
				format='json',
			).status_code,
			403,
		)
		self.assertEqual(
			self.client.patch(
				f'/api/menus/{menu.pk}/',
				{'nombre': 'Nombre cambiado'},
				format='json',
			).status_code,
			403,
		)
		self.assertEqual(self.client.delete(f'/api/menus/{menu.pk}/').status_code, 403)
		menu.refresh_from_db()
		self.assertEqual(menu.nombre, 'Menú existente')

	def test_administrator_role_can_manage_menus(self):
		role = Rol.objects.create(nombre='Administrador', estado=True)
		regular_user = Usuario.objects.create_user(
			usuario='role-admin',
			password='Password-548!',
		)
		UsuarioRol.objects.create(usuario=regular_user, rol=role)
		self.client.force_authenticate(user=regular_user)

		permissions_response = self.client.get('/api/menus/permissions/')
		self.assertEqual(permissions_response.status_code, 200)
		self.assertTrue(permissions_response.data['is_admin'])

		create_response = self.client.post(
			'/api/menus/',
			{'nombre': 'Menú de administrador', 'estado': True},
			format='json',
		)
		self.assertEqual(create_response.status_code, 201, create_response.data)
