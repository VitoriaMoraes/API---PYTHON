from django.http import HttpRequest, JsonResponse
from ninja import ModelSchema, NinjaAPI, Schema, UploadedFile, File
from .models import Cliente
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.core.files.base import ContentFile
from typing import List
import orjson
from PIL import Image
from ninja.parser import Parser
from django.http import HttpRequest

'''class ORJSONParser(Parser):
    def parse_body(self, request: HttpRequest):
        return orjson.loads(request.body)'''

api = NinjaAPI()


#Schema para ciração de usuário
class ClienteSchema(ModelSchema):
    class Config:
        model = Cliente
        model_fields = ['nome','telefone','cpf','email','senha', 'foto']

class ClienteIn(Schema):
    nome = str
    telefone = int
    senha = str

class ClientOut(Schema):
    nome = str
    telefone = str
    cpf = str
    email = str
    senha = str

#criar usuário 
@api.post('cliente')
def criar_cliente(request, cliente: ClienteSchema, imagem: UploadedFile = File(None)):
    image_data = imagem.read()
    NovoCliente = Cliente.objects.create(
        nome = cliente.nome,
        telefone = cliente.telefone,
        cpf = cliente.cpf,
        email = cliente.email,
        senha = cliente.senha,
        foto = ContentFile(image_data, name = imagem.name)
    )
    NovoCliente.save()
    return {"mensagem": "Usuario Cadastrado"}

#buscar
@api.get('cliente/', response=List[ClienteSchema])
def listar_todos(request):
    return Cliente.objects.all()

#buscar por id
@api.get('cliente/{id}', response=ClienteSchema)
def listar_por_id(request, id: int):
    cliente = Cliente.objects.get(id=id)
    return cliente

#buscar por nome
@api.get('cliente/nome/{nome}')
def listar_por_nome(request, nome: str):
    clienteNome = Cliente.objects.get(nome=nome)
    return {'mensagem':'usuario encontrado '}

#editar todos os dados 
@api.post('cliente/editar/{id}')
def editar_dados(request, id:int, nome : str, telefone: str, cpf: str, email: str, senha: str, foto: UploadedFile = File(None)):
    imagem = foto.read()
    dado = get_object_or_404(Cliente, id=id)
    if dado:
        dado.nome = nome
    if dado:
        dado.telefone = telefone
    if dado:
        dado.cpf = cpf
    if dado:
        dado.email = email
    if dado:
        dado.senha = senha
    if dado:
        dado.foto = ContentFile(imagem, name = imagem.name)
    dado.save()
    return {'mensagem':'seu dados foram modificados!'}

#atualizar nome
@api.patch('cliente/atualizar/nome/{id}')
def editar_nome(request, id:int, nome :  str):
    dado = get_object_or_404(Cliente, id=id)
    if dado:
        dado.nome = nome
    dado.save()
    return {'mensagem':'seu nome foi modificado!'}

#atualizar telefone
@api.patch('cliente/atualizar/tel/{id}')
def editar_telefone(request, id:int, telefone :  str):
    dado = get_object_or_404(Cliente, id=id)
    if dado:
        dado.telefone = telefone
    dado.save()
    return {'mensagem':'seu telefone foi modificado!'}

#atualizar cpf
@api.patch('cliente/atualizar/cpf/{id}')
def editar_cpf(request, id:int, cpf :  str):
    dado = get_object_or_404(Cliente, id=id)
    if dado:
        dado.cpf = cpf
    dado.save()
    return {'mensagem':'seu cpf foi modificado!'}

#atualizar email
@api.patch('cliente/atualizar/e-mail/{id}')
def editar_email(request, id:int, email :  str):
    dado = get_object_or_404(Cliente, id=id)
    if dado:
        dado.email = email
    dado.save()
    return {'mensagem':'seu email foi modificado!'}

#atualizar senha
@api.patch('cliente/atualizar/senha/{id}')
def editar_senha(request, id:int, senha :  str):
    dado = get_object_or_404(Cliente, id=id)
    if dado:
        dado.senha = senha
    dado.save()
    return {'mensagem':'sua senha foi modificada!'}

#atualizar imagem
@api.post('cliente/atualizar/foto/{id}')
def editar_foto(request, id:int, imagem: UploadedFile = File(None)):
    imagem_data = imagem.read()
    cliente = get_object_or_404(Cliente, id=id)
    if cliente:
        cliente.foto = ContentFile(imagem_data, name = imagem.name)
    cliente.save()
    return {"mensagem":"sua foto foi atualizada"}

#deletar
@api.delete('cliente/deletar/{id}')
def deletar(request, id:int):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    return {'mensagem':'o cliente foi deletado'}

