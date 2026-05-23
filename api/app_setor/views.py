from rest_framework import viewsets
from .models import Setor
from .serializers import SetorSerializer
from app_core.mixins import EmpresaQuerysetMixin


class SetorViewSet(EmpresaQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = SetorSerializer

    def get_queryset(self):
        queryset = Setor.objects.select_related('empresa')
        return self.filter_by_empresa(queryset, empresa_field='empresa')
