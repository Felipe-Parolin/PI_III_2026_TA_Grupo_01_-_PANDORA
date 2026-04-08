from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import (
    Empresa,
    Setor,
    Perfil,
    Usuarios,
    Manual,
    Equipamento,
    Ordem_servico,
    Anexo_OS,
    Analise_LLM,
)


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = '__all__'


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def create(self, validated_data):
        senha = validated_data.get('senha_hash')
        if senha:
            validated_data['senha_hash'] = make_password(senha)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        senha = validated_data.get('senha_hash')
        if senha:
            validated_data['senha_hash'] = make_password(senha)
        return super().update(instance, validated_data)


class ManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manual
        fields = '__all__'


class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = '__all__'


class OrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordem_servico
        fields = '__all__'


class AnexoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo_OS
        fields = '__all__'


class AnaliseLLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analise_LLM
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField()
