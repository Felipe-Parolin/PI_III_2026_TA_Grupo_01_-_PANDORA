from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 
from django.shortcuts import get_object_or_404

from pandora.models import AnaliseLLM, OrdemServico
from pandora.serializers import AnaliseLLMSerializer
from ..services import (
    GroqServiceError,
    analisar_com_groq,
    sugerir_solucao_os_com_groq,
    transcrever_audio,
)
import tempfile
import os

class AnaliseLLMViewSet(viewsets.ModelViewSet):
    queryset = AnaliseLLM.objects.all()
    serializer_class = AnaliseLLMSerializer
    permission_classes = [AllowAny] # Permite testar sem estar logado

    @action(detail=False, methods=['post'])
    def analisar(self, request):
        descricao = request.data.get('descricao')
        if not descricao:
            return Response({"error": "Descrição vazia"}, status=status.HTTP_400_BAD_REQUEST)
            
        resultado = analisar_com_groq(
            descricao,
            historico_equipamento=request.data.get('historico_equipamento') or [],
            contexto_os=f"OS vinculada: {request.data.get('os_id') or 'N/A'}",
        )
        return Response(resultado)

    @action(detail=False, methods=['post'], url_path='sugerir-solucao-os')
    def sugerir_solucao_os(self, request):
        os_id = request.data.get('os_id')
        if not os_id:
            return Response({"error": "OS nao informada"}, status=status.HTTP_400_BAD_REQUEST)

        ordem = get_object_or_404(
            OrdemServico.objects.select_related('equipamento__setor'),
            pk=os_id,
        )

        historico_queryset = (
            OrdemServico.objects
            .filter(equipamento_id=ordem.equipamento_id)
            .exclude(pk=ordem.pk)
            .order_by('-data_abertura')[:8]
        )
        historico = [
            {
                'id': item.id,
                'status': item.status,
                'urgencia': item.urgencia,
                'problema': item.descricao_problema,
                'solucao': item.descricao_solucao,
                'data_abertura': item.data_abertura.isoformat() if item.data_abertura else None,
                'data_fechamento': item.data_fechamento.isoformat() if item.data_fechamento else None,
            }
            for item in historico_queryset
        ]

        os_data = {
            'id': ordem.id,
            'status': ordem.status,
            'urgencia': ordem.urgencia,
            'descricao_problema': ordem.descricao_problema,
            'equipamento_nome': ordem.equipamento.nome_equipamento if ordem.equipamento else None,
            'equipamento_id_interno': ordem.equipamento.id_interno if ordem.equipamento else None,
            'equipamento_qr_token': ordem.equipamento.qr_code_token if ordem.equipamento else None,
            'equipamento_tipo': ordem.equipamento.tipo_equipamento if ordem.equipamento else None,
            'equipamento_setor_nome': ordem.equipamento.setor.nome_setor if ordem.equipamento else None,
        }

        try:
            resultado = sugerir_solucao_os_com_groq(os_data, historico)
            resultado['historico_considerado'] = len(historico)
            return Response(resultado)
        except GroqServiceError as e:
            return Response({'error': str(e)}, status=e.status_code)

    @action(detail=False, methods=['post'])
    def transcrever(self, request):
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({"error": "Áudio não enviado"}, status=status.HTTP_400_BAD_REQUEST)

        ext = os.path.splitext(audio_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            texto = transcrever_audio(tmp_path)
            if texto is None:
                return Response(
                    {'error': 'Não foi possível transcrever o áudio.'},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            return Response({'transcricao': texto if texto else ""})
        except GroqServiceError as e:
            return Response({'error': str(e)}, status=e.status_code)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
