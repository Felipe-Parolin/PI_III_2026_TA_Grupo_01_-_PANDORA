from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from pandora.models import HistoricoOS
from pandora.serializers import HistoricoOSSerializer


class HistoricoOSViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = HistoricoOSSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = HistoricoOS.objects.select_related(
            'os',
            'usuario_modificacao',
            'os__usuario_abertura',
            'os__usuario_tecnico',
        ).order_by('-data_modificacao')

        params = self.request.query_params

        os_id = params.get('os')
        if os_id:
            queryset = queryset.filter(os__id=os_id)

        campo = params.get('campo_alterado')
        if campo:
            queryset = queryset.filter(campo_alterado__icontains=campo)

        usuario_id = params.get('usuario_modificacao')
        if usuario_id:
            queryset = queryset.filter(usuario_modificacao__id=usuario_id)

        data_inicio = params.get('data_inicio')
        if data_inicio:
            queryset = queryset.filter(data_modificacao__date__gte=data_inicio)

        data_fim = params.get('data_fim')
        if data_fim:
            queryset = queryset.filter(data_modificacao__date__lte=data_fim)

        return queryset
