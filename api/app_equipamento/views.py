from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Equipamento
from .serializers import EquipamentoSerializer
from app_core.mixins import EmpresaQuerysetMixin


class EquipamentoViewSet(EmpresaQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = EquipamentoSerializer

    def get_queryset(self):
        queryset = Equipamento.objects.select_related('setor__empresa')
        return self.filter_by_empresa(queryset, empresa_field='setor__empresa')

    def perform_create(self, serializer):
        serializer.save()
