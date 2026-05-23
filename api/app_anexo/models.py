from django.db import models
from app_os.models import OrdemServico

class AnexoOS(models.Model):
    caminho_arquivo = models.FileField(upload_to='anexos_os/')
    nome_arquivo = models.CharField(max_length=255)
    os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='anexos')

    class Meta:
        app_label = 'app_anexo'

    def __str__(self):
        return self.nome_arquivo