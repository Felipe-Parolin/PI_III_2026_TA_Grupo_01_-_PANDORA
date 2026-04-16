from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .empresa import Empresa
from .setor import Setor
from .grupo import Grupo

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            raise ValueError('A senha é obrigatória')

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('ativo', True)

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nome_usuario = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    ativo = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT, related_name='usuarios')
    setor = models.ForeignKey(Setor, on_delete=models.RESTRICT, related_name='usuarios')
    grupos = models.ManyToManyField(Grupo, related_name='usuarios')

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_usuario']

    def __str__(self):
        return self.nome_usuario

    @property
    def is_active(self):
        return self.ativo