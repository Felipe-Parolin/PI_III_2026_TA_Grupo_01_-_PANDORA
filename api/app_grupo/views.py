from rest_framework import viewsets
from .models import Grupo
from .serializers import GrupoSerializer
from app_core.mixins import EmpresaQuerysetMixin


class GrupoViewSet(EmpresaQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = GrupoSerializer

    def get_queryset(self):
        queryset = Grupo.objects.select_related('empresa')
        return self.filter_by_empresa(queryset, empresa_field='empresa')
