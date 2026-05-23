from django.db import models
from app_empresa.models import Empresa
from app_permissao.models import Permissao

class Grupo(models.Model):
    nome_grupo = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, related_name='grupos')
    permissoes = models.ManyToManyField(Permissao, related_name='grupos')

    class Meta:
        app_label = 'app_grupo'

    def __str__(self):
        return self.nome_grupo