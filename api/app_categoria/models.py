from django.db import models

class CategoriaDocumento(models.Model):
    nome_categoria = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'app_categoria'

    def __str__(self):
        return self.nome_categoria