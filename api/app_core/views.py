from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from app_empresa.models import Empresa
from app_setor.models import Setor
from app_permissao.models import Permissao
from app_grupo.models import Grupo
from app_usuario.models import Usuario


class OnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {'detail': 'Acesso negado.'},
                status=status.HTTP_403_FORBIDDEN
            )

        dados = request.data
        nome_fantasia = dados.get('nome_fantasia')
        cnpj = dados.get('cnpj')
        nome_usuario = dados.get('nome_usuario')
        email = dados.get('email')
        senha = dados.get('senha')

        if not all([nome_fantasia, cnpj, nome_usuario, email, senha]):
            return Response(
                {'detail': 'Todos os campos são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Empresa.objects.filter(cnpj=cnpj).exists():
            return Response(
                {'detail': 'Já existe uma empresa cadastrada com este CNPJ.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Usuario.objects.filter(email=email).exists():
            return Response(
                {'detail': 'Já existe um usuário cadastrado com este e-mail.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                empresa = Empresa.objects.create(
                    nome_fantasia=nome_fantasia,
                    cnpj=cnpj
                )

                setor = Setor.objects.create(
                    nome_setor='Administrativo',
                    empresa=empresa
                )

                todas_permissoes = Permissao.objects.all()
                grupo = Grupo.objects.create(
                    nome_grupo='ADM',
                    empresa=empresa
                )
                grupo.permissoes.set(todas_permissoes)

                usuario = Usuario.objects.create_user(
                    email=email,
                    password=senha,
                    nome_usuario=nome_usuario,
                    empresa=empresa,
                    setor=setor,
                    ativo=True,
                )
                usuario.grupos.set([grupo])

            return Response({
                'detail': 'Cliente cadastrado com sucesso.',
                'empresa': empresa.nome_fantasia,
                'usuario': usuario.email,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'detail': f'Erro ao cadastrar: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )