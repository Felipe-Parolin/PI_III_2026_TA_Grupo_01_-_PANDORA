from django.db import models
from .setor import Setor

class Equipamento(models.Model):
    nome_equipamento = models.CharField(max_length=255)
    tipo_equipamento = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    id_interno = models.IntegerField()
    qr_code_token = models.CharField(max_length=255, unique=True)
    setor = models.ForeignKey(Setor, on_delete=models.RESTRICT, related_name='equipamentos')

    def __str__(self):
        return self.nome_equipamento