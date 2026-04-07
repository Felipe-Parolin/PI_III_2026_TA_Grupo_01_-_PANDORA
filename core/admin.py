from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import *

admin.site.register(Empresa)
admin.site.register(Setor)
admin.site.register(Perfil)
@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_usuario', 'email', 'empresa', 'perfil', 'setor', 'ativo')

    def save_model(self, request, obj, form, change):
        if 'senha_hash' in form.changed_data:
            obj.senha_hash = make_password(obj.senha_hash)
        super().save_model(request, obj, form, change)
admin.site.register(Manual)
admin.site.register(Equipamento)
admin.site.register(Ordem_servico)
admin.site.register(Anexo_OS)
admin.site.register(Analise_LLM)