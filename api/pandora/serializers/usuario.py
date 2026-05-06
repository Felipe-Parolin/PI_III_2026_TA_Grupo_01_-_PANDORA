from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from pandora.models import Usuario
from .empresa import EmpresaSerializer
from .setor import SetorSerializer
from .grupo import GrupoSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'nome_usuario',
            'email',
            'password',
            'ativo',
            'is_staff',
            'is_superuser',
            'empresa',
            'setor',
            'grupos',
        ]

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Este campo é obrigatório.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        grupos = validated_data.pop('grupos', [])
        usuario = Usuario.objects.create_user(password=password, **validated_data)

        if grupos:
            usuario.grupos.set(grupos)

        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        grupos = validated_data.pop('grupos', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if grupos is not None:
            instance.grupos.set(grupos)

        return instance


class UsuarioLoginSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    setor = SetorSerializer(read_only=True)
    grupos = GrupoSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'nome_usuario',
            'email',
            'ativo',
            'is_staff',
            'is_superuser',
            'empresa',
            'setor',
            'grupos',
        ]


class TrocarSenhaSerializer(serializers.Serializer):
    senha_atual = serializers.CharField(write_only=True, trim_whitespace=False)
    nova_senha = serializers.CharField(write_only=True, trim_whitespace=False)
    confirmar_senha = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        usuario = self.context['request'].user

        if not usuario.check_password(attrs['senha_atual']):
            raise serializers.ValidationError({'senha_atual': 'Senha atual incorreta.'})

        if attrs['nova_senha'] != attrs['confirmar_senha']:
            raise serializers.ValidationError({'confirmar_senha': 'As senhas nao conferem.'})

        if attrs['senha_atual'] == attrs['nova_senha']:
            raise serializers.ValidationError({'nova_senha': 'A nova senha deve ser diferente da senha atual.'})

        try:
            validate_password(attrs['nova_senha'], user=usuario)
        except DjangoValidationError as error:
            raise serializers.ValidationError({'nova_senha': list(error.messages)})

        return attrs

    def save(self, **kwargs):
        usuario = self.context['request'].user
        usuario.set_password(self.validated_data['nova_senha'])
        usuario.save(update_fields=['password'])
        return usuario
