from django.db import models

class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, unique=True)

    class Meta:
        app_label = 'app_empresa'

    def __str__(self):
        return self.nome_fantasia