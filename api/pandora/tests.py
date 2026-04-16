from django.contrib.auth import authenticate
from django.test import TestCase

from pandora.models import Empresa, Grupo, Setor, Usuario
from pandora.serializers.usuario import UsuarioSerializer


class UsuarioSerializerTests(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome_fantasia='Empresa Teste',
            cnpj='00.000.000/0001-00',
        )
        self.setor = Setor.objects.create(
            nome_setor='TI',
            empresa=self.empresa,
        )
        self.grupo = Grupo.objects.create(
            nome_grupo='Administradores',
            empresa=self.empresa,
        )

    def test_create_hashes_password_and_allows_login(self):
        serializer = UsuarioSerializer(data={
            'nome_usuario': 'Maria',
            'email': 'maria@example.com',
            'password': 'senha123',
            'ativo': True,
            'empresa': self.empresa.id,
            'setor': self.setor.id,
            'grupos': [self.grupo.id],
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)
        usuario = serializer.save()

        self.assertNotEqual(usuario.password, 'senha123')
        self.assertTrue(usuario.check_password('senha123'))
        self.assertEqual(usuario.grupos.count(), 1)
        self.assertIsNotNone(authenticate(username='maria@example.com', password='senha123'))

    def test_update_hashes_new_password(self):
        usuario = Usuario.objects.create_user(
            email='joao@example.com',
            password='antiga123',
            nome_usuario='João',
            empresa=self.empresa,
            setor=self.setor,
        )

        serializer = UsuarioSerializer(
            usuario,
            data={'password': 'nova12345'},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        usuario = serializer.save()

        self.assertTrue(usuario.check_password('nova12345'))
        self.assertIsNotNone(authenticate(username='joao@example.com', password='nova12345'))
