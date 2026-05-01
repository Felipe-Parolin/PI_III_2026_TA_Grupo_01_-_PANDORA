from rest_framework import serializers
from pandora.models import DocumentoEquipamento

class DocumentoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoEquipamento
        fields = '__all__'
        # Tornamos 'categoria' opcional no serializer para não quebrar
        # caso o frontend não envie. Se categoria for sempre obrigatória
        # no seu fluxo, remova o extra_kwargs abaixo.
        extra_kwargs = {
            'categoria': {'required': False, 'allow_null': True}
        }