from rest_framework import serializers
from .models import DocumentoEquipamento

class DocumentoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoEquipamento
        fields = '__all__'