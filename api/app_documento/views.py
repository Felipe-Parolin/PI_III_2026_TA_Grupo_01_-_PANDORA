from rest_framework import viewsets
from .models import DocumentoEquipamento
from .serializers import DocumentoEquipamentoSerializer
from app_core.mixins import EmpresaQuerysetMixin


class DocumentoEquipamentoViewSet(EmpresaQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = DocumentoEquipamentoSerializer

    def get_queryset(self):
        queryset = DocumentoEquipamento.objects.select_related(
            'equipamento__setor__empresa'
        )
        return self.filter_by_empresa(queryset, empresa_field='equipamento__setor__empresa')
