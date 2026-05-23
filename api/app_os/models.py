from django.db import models
from app_usuario.models import Usuario
from app_equipamento.models import Equipamento
from app_empresa.models import Empresa

class OrdemServico(models.Model):
    data_abertura = models.DateTimeField(auto_now_add=True)
    urgencia = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    descricao_problema = models.TextField()
    foto_problema = models.ImageField(upload_to='os/problemas/', null=True, blank=True)
    usuario_abertura = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='os_abertas')
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='ordens_servico')
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, related_name='ordens_servico', null=True, blank=True)
    usuario_tecnico = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='os_atendidas', null=True, blank=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    descricao_solucao = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'app_os'

    def __str__(self):
        return f"OS {self.id} - {self.equipamento.nome_equipamento}"