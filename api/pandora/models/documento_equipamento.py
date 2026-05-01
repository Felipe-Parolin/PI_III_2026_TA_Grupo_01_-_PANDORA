from django.db import models
from .equipamento import Equipamento
from .categoria_documento import CategoriaDocumento

class DocumentoEquipamento(models.Model):
    caminho_arquivo = models.FileField(upload_to='documentos_equipamentos/')
    nome_arquivo = models.CharField(max_length=255)
    # null=True, blank=True torna a categoria opcional,
    # permitindo uploads sem precisar informar uma categoria.
    # Se quiser categoria obrigatória, remova esses dois argumentos.
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

    def __str__(self):
        return self.nome_arquivo