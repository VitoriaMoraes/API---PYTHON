from django.db import models

class Cliente(models.Model):
    # Django cria automaticamente um campo id como chave primária mesmo sem especificar explicitamente um.
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=60)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=128)
    foto = models.ImageField(upload_to= 'imagem/')

    def __str__(self):
        return self.nome
    
class Profissional(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=60)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=128)
    cpf = models.CharField(max_length=11, unique=True)
    endereco = models.CharField(max_length=60)
    foto = models.ImageField(upload_to= 'imagem/')
    banner = models.ImageField(upload_to= 'imagem/banner/')

    def __str__(self):
        return self.nome