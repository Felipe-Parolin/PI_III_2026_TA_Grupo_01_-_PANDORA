from django.db import models
from app_equipamento.models import Equipamento
from app_categoria.models import CategoriaDocumento

class DocumentoEquipamento(models.Model):
    caminho_arquivo = models.FileField(upload_to='documentos_equipamentos/')
    nome_arquivo = models.CharField(max_length=255)
    categoria = models.ForeignKey(
        CategoriaDocumento,
        on_delete=models.RESTRICT,
        related_name='documentos',
        null=True,
        blank=True
    )
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE,
        related_name='documentos'
    )

    class Meta:
        app_label = 'app_documento'

    def __str__(self):
        return self.nome_arquivo