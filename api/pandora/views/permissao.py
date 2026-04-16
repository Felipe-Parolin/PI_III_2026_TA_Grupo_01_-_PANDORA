from rest_framework import viewsets
from pandora.models import Permissao
from pandora.serializers import PermissaoSerializer

class PermissaoViewSet(viewsets.ModelViewSet):
    queryset = Permissao.objects.all()
    serializer_class = PermissaoSerializer