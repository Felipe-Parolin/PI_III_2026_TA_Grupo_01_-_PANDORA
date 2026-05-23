from rest_framework import serializers
from .models import CategoriaDocumento

class CategoriaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaDocumento
        fields = '__all__'