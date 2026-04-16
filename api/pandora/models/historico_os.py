from django.db import models
from .ordem_servico import OrdemServico
from .usuario import Usuario

class HistoricoOS(models.Model):
    data_modificacao = models.DateTimeField(auto_now_add=True)
    campo_alterado = models.CharField(max_length=255)
    valor_anterior = models.CharField(max_length=255, null=True, blank=True)
    valor_novo = models.CharField(max_length=255, null=True, blank=True)
    os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='historico')
    usuario_modificacao = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='modificacoes')

    def __str__(self):
        return f"Alteração em {self.campo_alterado} - OS {self.os.id}"