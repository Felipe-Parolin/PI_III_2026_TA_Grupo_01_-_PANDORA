from rest_framework import viewsets
from pandora.models import AnaliseLLM
from pandora.serializers import AnaliseLLMSerializer

class AnaliseLLMViewSet(viewsets.ModelViewSet):
    queryset = AnaliseLLM.objects.all()
    serializer_class = AnaliseLLMSerializer