from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from pandora.serializers.usuario import UsuarioLoginSerializer

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
