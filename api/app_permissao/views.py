from rest_framework import viewsets
from .models import Permissao
from .serializers import PermissaoSerializer

class PermissaoViewSet(viewsets.ModelViewSet):
    queryset = Permissao.objects.all()
    serializer_class = PermissaoSerializer