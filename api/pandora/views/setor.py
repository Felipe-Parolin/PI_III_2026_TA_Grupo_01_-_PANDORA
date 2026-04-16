from rest_framework import viewsets
from pandora.models import Setor
from pandora.serializers import SetorSerializer

class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer