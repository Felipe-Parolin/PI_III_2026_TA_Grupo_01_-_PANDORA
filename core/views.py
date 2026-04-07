from django.shortcuts import render

# Create your views here.
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    Empresa,
    Setor,
    Perfil,
    Usuarios,
    Manual,
    Equipamento,
    Ordem_servico,
    Anexo_OS,
    Analise_LLM,
)
from .serializers import (
    EmpresaSerializer,
    SetorSerializer,
    PerfilSerializer,
    UsuariosSerializer,
    ManualSerializer,
    EquipamentoSerializer,
    OrdemServicoSerializer,
    AnexoOSSerializer,
    AnaliseLLMSerializer,
    LoginSerializer,
)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer


class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer


class ManualViewSet(viewsets.ModelViewSet):
    queryset = Manual.objects.all()
    serializer_class = ManualSerializer


class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer


class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = Ordem_servico.objects.all()
    serializer_class = OrdemServicoSerializer


class AnexoOSViewSet(viewsets.ModelViewSet):
    queryset = Anexo_OS.objects.all()
    serializer_class = AnexoOSSerializer


class AnaliseLLMViewSet(viewsets.ModelViewSet):
    queryset = Analise_LLM.objects.all()
    serializer_class = AnaliseLLMSerializer

@api_view(['POST'])
def login_usuario(request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    senha = serializer.validated_data['senha']

    try:
        usuario = Usuarios.objects.select_related('perfil', 'setor').get(email=email)
    except Usuarios.DoesNotExist:
        return Response(
            {'erro': 'Usuário não encontrado.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not check_password(senha, usuario.senha_hash):
        return Response(
            {'erro': 'Senha inválida.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return Response({
        'mensagem': 'Login realizado com sucesso.',
        'usuario': {
            'id': usuario.id,
            'nome_usuario': usuario.nome_usuario,
            'email': usuario.email,
            'ativo': usuario.ativo,
            'empresa': {
                'id': usuario.empresa.id,
                'nome_fantasia': usuario.empresa.nome_fantasia
            },
            'perfil': {
                'id': usuario.perfil.id,
                'tipo_perfil': usuario.perfil.tipo_perfil
            },
            'setor': {
                'id': usuario.setor.id,
                'nome_setor': usuario.setor.nome_setor
            } if usuario.setor else None
        }
    })