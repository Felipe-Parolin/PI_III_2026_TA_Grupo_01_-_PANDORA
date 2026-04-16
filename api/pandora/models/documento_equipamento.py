from django.db import models
from .equipamento import Equipamento
from .categoria_documento import CategoriaDocumento

class DocumentoEquipamento(models.Model):
    caminho_arquivo = models.FileField(upload_to='documentos_equipamentos/')
    nome_arquivo = models.CharField(max_length=255)
    categoria = models.ForeignKey(CategoriaDocumento, on_delete=models.RESTRICT, related_name='documentos')
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='documentos')

    def __str__(self):
        return self.nome_arquivo