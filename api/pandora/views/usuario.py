from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pandora.models import Usuario
from pandora.serializers import TrocarSenhaSerializer, UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

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
