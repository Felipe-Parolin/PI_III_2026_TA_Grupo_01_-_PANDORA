from rest_framework import serializers
from pandora.models import OrdemServico

class OrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemServico
        fields = '__all__'