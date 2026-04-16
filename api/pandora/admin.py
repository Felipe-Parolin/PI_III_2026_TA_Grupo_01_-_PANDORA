from django.contrib import admin
from .models import (
    Empresa,
    Setor,
    Permissao,
    Grupo,
    Usuario,
    Equipamento,
    OrdemServico,
    CategoriaDocumento,
    DocumentoEquipamento,
    AnexoOS,
    AnaliseLLM,
    HistoricoOS,
)

admin.site.register(Empresa)
admin.site.register(Setor)
admin.site.register(Permissao)
admin.site.register(Grupo)
admin.site.register(Usuario)
admin.site.register(Equipamento)
admin.site.register(OrdemServico)
admin.site.register(CategoriaDocumento)
admin.site.register(DocumentoEquipamento)
admin.site.register(AnexoOS)
admin.site.register(AnaliseLLM)
admin.site.register(HistoricoOS)