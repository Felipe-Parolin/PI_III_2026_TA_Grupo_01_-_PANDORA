from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from pandora.models import Usuario

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        email = self.initial_data.get('email', attrs.get('username'))
        
        try:
            usuario = Usuario.objects.get(email=email)
            data['usuario'] = {
                'id': usuario.id,
                'nome_usuario': usuario.nome_usuario,
                'empresa_id': getattr(usuario, 'empresa_id', None)
            }
            
            permissoes_lista = []
            for grupo in usuario.grupos.all():
                for permissao in grupo.permissoes.all():
                    permissoes_lista.append(permissao.nome_permissao)
                    
            data['permissoes'] = list(set(permissoes_lista))
        except Usuario.DoesNotExist:
            pass
            
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer