from django.db import models
from .empresa import Empresa
from .permissao import Permissao

class Grupo(models.Model):
    nome_grupo = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, related_name='grupos')
    permissoes = models.ManyToManyField(Permissao, related_name='grupos')

    def __str__(self):
        return self.nome_grupo