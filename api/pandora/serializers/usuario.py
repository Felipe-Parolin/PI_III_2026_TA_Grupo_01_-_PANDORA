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
