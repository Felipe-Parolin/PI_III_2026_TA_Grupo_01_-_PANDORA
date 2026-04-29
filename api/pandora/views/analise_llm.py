from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 

from pandora.models import AnaliseLLM
from pandora.serializers import AnaliseLLMSerializer
from ..services import analisar_com_groq, transcrever_audio
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
            
        resultado = analisar_com_groq(descricao)
        return Response(resultado)

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
            return Response({'transcricao': texto if texto else ""})
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)