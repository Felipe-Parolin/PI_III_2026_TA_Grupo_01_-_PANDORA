from rest_framework import serializers
from pandora.models import CategoriaDocumento

class CategoriaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaDocumento
        fields = '__all__'