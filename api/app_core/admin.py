from django.contrib import admin
from app_empresa.models import Empresa
from app_setor.models import Setor
from app_permissao.models import Permissao
from app_grupo.models import Grupo
from app_usuario.models import Usuario
from app_equipamento.models import Equipamento
from app_os.models import OrdemServico
from app_categoria.models import CategoriaDocumento
from app_documento.models import DocumentoEquipamento
from app_anexo.models import AnexoOS
from app_analise.models import AnaliseLLM
from app_historico.models import HistoricoOS

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