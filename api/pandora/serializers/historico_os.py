from rest_framework import serializers
from pandora.models import HistoricoOS

class HistoricoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoOS
        fields = '__all__'