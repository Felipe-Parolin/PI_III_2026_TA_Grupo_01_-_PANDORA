from rest_framework import viewsets
from .models import CategoriaDocumento
from .serializers import CategoriaDocumentoSerializer
from app_core.mixins import EmpresaQuerysetMixin


class CategoriaDocumentoViewSet(EmpresaQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = CategoriaDocumentoSerializer

    def get_queryset(self):
        queryset = CategoriaDocumento.objects.all()
        return queryset
