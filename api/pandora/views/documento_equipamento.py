from rest_framework import viewsets
from pandora.models import DocumentoEquipamento
from pandora.serializers import DocumentoEquipamentoSerializer

class DocumentoEquipamentoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoEquipamento.objects.all()
    serializer_class = DocumentoEquipamentoSerializer