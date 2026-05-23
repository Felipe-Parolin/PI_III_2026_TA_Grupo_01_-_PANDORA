from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Usuario
from .serializers import TrocarSenhaSerializer, UsuarioSerializer, UsuarioLoginSerializer
from app_core.mixins import EmpresaQuerysetMixin


class UsuarioViewSet(EmpresaQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        queryset = Usuario.objects.select_related('empresa', 'setor').prefetch_related('grupos')
        return self.filter_by_empresa(queryset, empresa_field='empresa')

    @action(
        detail=False,
        methods=['post'],
        url_path='trocar-senha',
        permission_classes=[IsAuthenticated],
    )
    def trocar_senha(self, request):
        serializer = TrocarSenhaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'detail': 'Email e senha são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response(
                {'detail': 'Credenciais inválidas.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not user.is_active:
            return Response(
                {'detail': 'Usuário inativo.'},
                status=status.HTTP_403_FORBIDDEN
            )
        refresh = RefreshToken.for_user(user)
        usuario_serializado = UsuarioLoginSerializer(user).data
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'usuario': usuario_serializado,
        })


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        email = self.initial_data.get('email', attrs.get('username'))
        try:
            usuario = Usuario.objects.get(email=email)
            data['usuario'] = {
                'id': usuario.id,
                'nome_usuario': usuario.nome_usuario,
                'empresa_id': getattr(usuario, 'empresa_id', None),
                'is_superuser': usuario.is_superuser,
            }
            permissoes_lista = []
            for grupo in usuario.grupos.all():
                for permissao in grupo.permissoes.all():
                    permissoes_lista.append(permissao.nome_permissao)
            data['permissoes'] = list(set(permissoes_lista))
        except Usuario.DoesNotExist:
            pass
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
