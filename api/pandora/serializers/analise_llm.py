from rest_framework import serializers
from pandora.models import AnaliseLLM

class AnaliseLLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnaliseLLM
        fields = '__all__'