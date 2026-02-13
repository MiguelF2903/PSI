from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from io import StringIO


class CreateSuCommandTest(TestCase):
    def test_createsu_creates_superuser(self):
        # Asegurarse de que no existe antes del test
        User.objects.filter(username='alumnodb').delete()

        out = StringIO()
        call_command('createsu', stdout=out)

        self.assertTrue(User.objects.filter(username='alumnodb').exists())
        u = User.objects.get(username='alumnodb')
        self.assertTrue(u.is_superuser)
        self.assertTrue(u.is_staff)
        self.assertIn('Superuser created successfully', out.getvalue())

    def test_createsu_already_exists(self):
        # Crear usuario primero para probar idempotencia
        if not User.objects.filter(username='alumnodb').exists():
            User.objects.create_superuser(
                'alumnodb', 'alumnodb@example.com', 'alumnodb')

        out = StringIO()
        call_command('createsu', stdout=out)

        self.assertIn('Superuser already exists', out.getvalue())
