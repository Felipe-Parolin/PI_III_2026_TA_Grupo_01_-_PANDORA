from django.db import models
from .empresa import Empresa

class Setor(models.Model):
    nome_setor = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, related_name='setores')

    def __str__(self):
        return self.nome_setor