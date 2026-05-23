from django.db import models
from app_setor.models import Setor
from app_empresa.models import Empresa

class Equipamento(models.Model):
    nome_equipamento = models.CharField(max_length=255)
    tipo_equipamento = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    id_interno = models.IntegerField()
    qr_code_token = models.CharField(max_length=255, unique=True)
    setor = models.ForeignKey(Setor, on_delete=models.RESTRICT, related_name='equipamentos')
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, related_name='equipamentos', null=True, blank=True)
    foto = models.ImageField(upload_to='equipamentos/fotos/', null=True, blank=True)
    manual_tecnico = models.FileField(upload_to='equipamentos/manuais/', null=True, blank=True)

    class Meta:
        app_label = 'app_equipamento'

    def __str__(self):
        return self.nome_equipamento