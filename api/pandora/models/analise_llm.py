from django.db import models
from .ordem_servico import OrdemServico
from .usuario import Usuario

class AnaliseLLM(models.Model):
    data_consulta = models.DateTimeField(auto_now_add=True)
    pergunta_prompt = models.TextField()
    resposta_ia = models.TextField()
    os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='analises_ia')
    usuario_consulta = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='analises_llm', null=True, blank=True)

    def __str__(self):
        return f"Análise LLM - OS {self.os.id}"