from rest_framework import serializers
from pandora.models import Equipamento

class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = '__all__'