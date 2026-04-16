from rest_framework import viewsets
from pandora.models import Empresa
from pandora.serializers import EmpresaSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer