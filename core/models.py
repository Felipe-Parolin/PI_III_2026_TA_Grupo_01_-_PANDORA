from django.db import models

class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self):
        return self.nome_fantasia

class Setor(models.Model):
    nome_setor = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='setores')

    def __str__(self):
        return self.nome_setor

class Perfil(models.Model):
    tipo_perfil = models.CharField(max_length=50) # Ex: Administrador, Manutenção, Produção

    def __str__(self):
        return self.tipo_perfil

class Usuarios(models.Model):
    nome_usuario = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha_hash = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuarios')
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_usuario

class Equipamento(models.Model):
    nome_equipamento = models.CharField(max_length=255)
    tipo_equipamento = models.CharField(max_length=100)
    criticidade = models.IntegerField()
    status_ativo = models.BooleanField(default=True)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    id_interno = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome_equipamento


class Manual(models.Model):
    tipo_arquivo = models.CharField(max_length=50)
    caminho_url = models.URLField(max_length=500)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='manuais')

    def __str__(self):
        return f"{self.tipo_arquivo} - {self.equipamento.nome_equipamento}"

class Ordem_servico(models.Model):
    data_abertura = models.DateTimeField(auto_now_add=True)
    urgencia = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    descricao = models.TextField()
    usuario_abertura = models.ForeignKey(Usuarios, on_delete=models.PROTECT, related_name='os_abertas')
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    usuario_tecnico = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True, related_name='os_atendidas')

    def __str__(self):
        return f"OS #{self.id} - {self.equipamento.nome_equipamento}"

class Anexo_OS(models.Model):
    tipo_anexo = models.CharField(max_length=50)
    caminho_url = models.URLField(max_length=500)
    os = models.ForeignKey(Ordem_servico, on_delete=models.CASCADE, related_name='anexos')

class Analise_LLM(models.Model):
    anomalia_detectada = models.TextField()
    causa_raiz = models.TextField()
    acao_sugerida = models.TextField()
    os = models.OneToOneField(Ordem_servico, on_delete=models.CASCADE) # Relação 1:1, pois cada OS tem 1 análise