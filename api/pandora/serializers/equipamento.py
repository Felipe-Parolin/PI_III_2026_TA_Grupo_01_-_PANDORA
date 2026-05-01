from rest_framework import serializers
from pandora.models import Equipamento, DocumentoEquipamento


class DocumentoEquipamentoInlineSerializer(serializers.ModelSerializer):
    # Retorna a URL absoluta do arquivo para o frontend conseguir abrir
    caminho_arquivo = serializers.SerializerMethodField()

    class Meta:
        model = DocumentoEquipamento
        fields = ['id', 'nome_arquivo', 'caminho_arquivo']

    def get_caminho_arquivo(self, obj):
        request = self.context.get('request')
        if obj.caminho_arquivo and request:
            return request.build_absolute_uri(obj.caminho_arquivo.url)
        return obj.caminho_arquivo.url if obj.caminho_arquivo else None


class EquipamentoSerializer(serializers.ModelSerializer):
    # Puxa todos os DocumentoEquipamento vinculados (related_name='documentos')
    documentos = DocumentoEquipamentoInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Equipamento
        fields = '__all__'