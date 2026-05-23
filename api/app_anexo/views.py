from rest_framework import viewsets
from .models import AnexoOS
from .serializers import AnexoOSSerializer
from app_core.mixins import EmpresaQuerysetMixin


class AnexoOSViewSet(EmpresaQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = AnexoOSSerializer

    def get_queryset(self):
        queryset = AnexoOS.objects.select_related(
            'os__equipamento__setor__empresa'
        )
        return self.filter_by_empresa(queryset, empresa_field='os__equipamento__setor__empresa')
