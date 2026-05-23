from rest_framework import serializers
from .models import AnexoOS

class AnexoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoOS
        fields = '__all__'