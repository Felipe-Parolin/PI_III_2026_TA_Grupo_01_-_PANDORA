from rest_framework import serializers
from .models import HistoricoOS

class HistoricoOSSerializer(serializers.ModelSerializer):
    os_id = serializers.IntegerField(source='os.id', read_only=True)
    usuario_nome = serializers.CharField(source='usuario_modificacao.nome_usuario', read_only=True)
    usuario_abertura_nome = serializers.CharField(source='os.usuario_abertura.nome_usuario', read_only=True)
    usuario_tecnico_nome = serializers.CharField(
        source='os.usuario_tecnico.nome_usuario', read_only=True, allow_null=True
    )
    os_comentario_tecnico = serializers.CharField(
        source='os.descricao_solucao', read_only=True, allow_null=True
    )
    os_status = serializers.CharField(source='os.status', read_only=True)
    os_data_fechamento = serializers.DateTimeField(
        source='os.data_fechamento', read_only=True, allow_null=True
    )

    class Meta:
        model = HistoricoOS
        fields = [
            'id', 'data_modificacao', 'comentario', 'campo_alterado',
            'valor_anterior', 'valor_novo', 'os', 'os_id',
            'usuario_modificacao', 'usuario_nome', 'usuario_abertura_nome',
            'usuario_tecnico_nome', 'os_comentario_tecnico', 'os_status', 'os_data_fechamento',
        ]
        read_only_fields = [
            'id', 'data_modificacao', 'os_id', 'usuario_nome',
            'usuario_abertura_nome', 'usuario_tecnico_nome',
            'os_comentario_tecnico', 'os_status', 'os_data_fechamento',
        ]