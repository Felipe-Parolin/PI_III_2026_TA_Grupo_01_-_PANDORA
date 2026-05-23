from django.db import models
from app_empresa.models import Empresa

class Setor(models.Model):
    nome_setor = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, related_name='setores')

    class Meta:
        app_label = 'app_setor'

    def __str__(self):
        return self.nome_setor