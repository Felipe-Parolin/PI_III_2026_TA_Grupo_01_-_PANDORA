from django.db import models

class Permissao(models.Model):
    nome_permissao = models.CharField(max_length=255)

    class Meta:
        app_label = 'app_permissao'

    def __str__(self):
        return self.nome_permissao