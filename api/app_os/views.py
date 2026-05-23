from rest_framework import viewsets
from app_historico.models import HistoricoOS
from .models import OrdemServico
from .serializers import OrdemServicoSerializer
from app_core.mixins import EmpresaQuerysetMixin

CAMPOS_RASTREADOS = [
    'status',
    'urgencia',
    'descricao_problema',
    'descricao_solucao',
    'usuario_tecnico_id',
    'data_fechamento',
]


def normalizar_valor(valor):
    if valor is None:
        return None
    return str(valor)


class OrdemServicoViewSet(EmpresaQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = OrdemServicoSerializer

    def get_queryset(self):
        queryset = OrdemServico.objects.select_related(
            'equipamento__setor__empresa',
            'usuario_abertura',
            'usuario_tecnico',
        )
        return self.filter_by_empresa(queryset, empresa_field='equipamento__setor__empresa')

    def _get_usuario_historico(self, instance):
        if getattr(self.request.user, 'is_authenticated', False):
            return self.request.user
        return instance.usuario_tecnico or instance.usuario_abertura

    def _registrar_historico(self, instance, campo, valor_anterior, valor_novo):
        HistoricoOS.objects.create(
            os=instance,
            usuario_modificacao=self._get_usuario_historico(instance),
            campo_alterado=campo,
            valor_anterior=normalizar_valor(valor_anterior),
            valor_novo=normalizar_valor(valor_novo),
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        self._registrar_historico(instance, 'status', None, instance.status)

    def perform_update(self, serializer):
        anterior = self.get_object()
        valores_anteriores = {
            campo: getattr(anterior, campo, None)
            for campo in CAMPOS_RASTREADOS
        }
        status_novo = self.request.data.get('status')
        if status_novo in ['Em Andamento', 'Concluido']:
            instance = serializer.save(usuario_tecnico=self.request.user)
        else:
            instance = serializer.save()
        for campo in CAMPOS_RASTREADOS:
            valor_anterior = valores_anteriores.get(campo)
            valor_novo = getattr(instance, campo, None)
            if normalizar_valor(valor_anterior) != normalizar_valor(valor_novo):
                self._registrar_historico(instance, campo, valor_anterior, valor_novo)
