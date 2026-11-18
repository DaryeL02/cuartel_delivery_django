from django.test import TestCase
from rest_framework.exceptions import ValidationError

from core.models import Empleado, Local
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

        self.assertEqual(serializer.fields['dni'].run_validation('12345678'), '12345678')
