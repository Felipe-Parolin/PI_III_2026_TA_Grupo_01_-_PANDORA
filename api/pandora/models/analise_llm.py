from django.db import models
from .ordem_servico import OrdemServico

class AnaliseLLM(models.Model):
    data_consulta = models.DateTimeField(auto_now_add=True)
    pergunta_prompt = models.TextField()
    resposta_ia = models.TextField()
    os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='analises_ia')

    def __str__(self):
        return f"Análise LLM - OS {self.os.id}"