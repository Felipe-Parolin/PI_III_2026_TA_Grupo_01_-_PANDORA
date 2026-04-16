from rest_framework import viewsets
from pandora.models import CategoriaDocumento
from pandora.serializers import CategoriaDocumentoSerializer

class CategoriaDocumentoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaDocumento.objects.all()
    serializer_class = CategoriaDocumentoSerializer