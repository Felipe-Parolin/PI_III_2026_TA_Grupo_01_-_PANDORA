from rest_framework import serializers
from pandora.models import DocumentoEquipamento

class DocumentoEquipamentoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.SerializerMethodField()

    class Meta:
        model = DocumentoEquipamento
        fields = [
            'id',
            'caminho_arquivo',
            'nome_arquivo',
            'categoria',
            'categoria_nome',
            'equipamento'
        ]
        # Tornamos 'categoria' opcional no serializer para não quebrar
        # caso o frontend não envie. Se categoria for sempre obrigatória
        # no seu fluxo, remova o extra_kwargs abaixo.
        extra_kwargs = {
            'categoria': {'required': False, 'allow_null': True}
        }

    def get_categoria_nome(self, obj):
        return obj.categoria.nome_categoria if obj.categoria else None
