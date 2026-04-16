from rest_framework import viewsets
from pandora.models import Grupo
from pandora.serializers import GrupoSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer