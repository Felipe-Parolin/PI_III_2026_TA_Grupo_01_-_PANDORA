from rest_framework import serializers
from pandora.models import OrdemServico


class OrdemServicoSerializer(serializers.ModelSerializer):
    usuario_abertura_nome  = serializers.CharField(source='usuario_abertura.nome_usuario', read_only=True)
    usuario_tecnico_nome   = serializers.CharField(source='usuario_tecnico.nome_usuario', read_only=True, allow_null=True)
    equipamento_nome       = serializers.CharField(source='equipamento.nome_equipamento', read_only=True)
    equipamento_id_interno = serializers.IntegerField(source='equipamento.id_interno', read_only=True)
    equipamento_qr_token   = serializers.CharField(source='equipamento.qr_code_token', read_only=True)
    equipamento_tipo       = serializers.CharField(source='equipamento.tipo_equipamento', read_only=True)
    equipamento_foto       = serializers.SerializerMethodField()
    equipamento_documentos = serializers.SerializerMethodField()
    
    # ADICIONE ESTE MÉTODO PARA A FOTO DO PROBLEMA
    foto_problema          = serializers.SerializerMethodField()

    class Meta:
        model = OrdemServico
        fields = '__all__'

    def get_foto_problema(self, obj):
        request = self.context.get('request')
        if obj.foto_problema and request:
            return request.build_absolute_uri(obj.foto_problema.url)
        return obj.foto_problema.url if obj.foto_problema else None

    def get_equipamento_foto(self, obj):
        request = self.context.get('request')
        foto = obj.equipamento.foto if obj.equipamento else None
        if foto and request:
            return request.build_absolute_uri(foto.url)
        return foto.url if foto else None

    def get_equipamento_documentos(self, obj):
        if not obj.equipamento:
            return []
        request = self.context.get('request')
        docs = obj.equipamento.documentos.all()
        result = []
        for doc in docs:
            url = None
            if doc.caminho_arquivo:
                url = request.build_absolute_uri(doc.caminho_arquivo.url) if request else doc.caminho_arquivo.url
            result.append({
                'id': doc.id,
                'nome_arquivo': doc.nome_arquivo,
                'caminho_arquivo': url,
            })
        return result