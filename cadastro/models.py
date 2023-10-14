from django.db import models

# AbstractUser herda automaticamente campos como email e senha associados a um usuário
class Cliente(models.Model):
    # Django cria automaticamente um campo id como chave primária mesmo sem especificar explicitamente um.
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=60)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=128)
    foto = models.ImageField(upload_to='cliente_fotos/', null=True)

    def __str__(self):
        return self.nome
