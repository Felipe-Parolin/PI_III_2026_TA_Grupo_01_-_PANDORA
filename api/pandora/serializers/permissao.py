from rest_framework import serializers
from pandora.models import Permissao

class PermissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissao
        fields = '__all__'