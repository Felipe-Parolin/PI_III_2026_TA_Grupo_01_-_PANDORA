from rest_framework import viewsets
from pandora.models import OrdemServico
from pandora.serializers import OrdemServicoSerializer

class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all()
    serializer_class = OrdemServicoSerializer

    def perform_update(self, serializer):
        # Captura o status enviado pelo frontend
        status_novo = self.request.data.get('status')
        
        # Se estiver assumindo ou finalizando, o Django salva quem é o usuário logado
        if status_novo in ['Em Andamento', 'Concluído']:
            # O campo usuario_tecnico recebe o objeto do usuário autenticado
            serializer.save(usuario_tecnico=self.request.user)
        else:
            serializer.save()