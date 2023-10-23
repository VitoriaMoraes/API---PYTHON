from django.http import HttpRequest, JsonResponse
from ninja import ModelSchema, NinjaAPI, Schema, UploadedFile, File
from .models import Cliente, Profissional
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.core.files.base import ContentFile
from typing import List
from PIL import Image
from django.core.exceptions import MultipleObjectsReturned
from ninja.parser import Parser
from django.http import HttpRequest
#import Schema 

api = NinjaAPI()


#Schema para criação do Cliente
class ClienteSchema(ModelSchema): #ClienteSchema será usado para definir como um objeto da classe Cliente deve ser serializado/desserializado usando o ModelSchema.
    class Config: #configura o Schema especificando quais campos devem ser incluídos no processo. 
        model = Cliente 
        model_fields = ['nome','telefone','cpf','email','senha', 'foto']

#Schema para criação do Profissional
class ProfissionalSchema(ModelSchema): #ProfissionalSchema será usado para definir como um objeto da classe Profissional deve ser serializado/desserializado usando o ModelSchema.
    class Config: #configura o Schema especificando quais campos devem ser incluídos no processo. 
        model = Profissional #modelo do tipo Profissional criado no banco de dados
        model_fields = ['nome','telefone','email','senha', 'cpf','foto','banner','endereco']


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



#PROFISSIONAL

#criar Profissional
@api.post('profissional')
def criar_profissional(request,profissional: ProfissionalSchema, foto: UploadedFile = File(None), banner: UploadedFile = File(None)):
    foto_data = foto.read()
    banner_data = banner.read()
    NovoProfissional = Profissional.objects.create(
        nome = profissional.nome,
        telefone = profissional.telefone,
        email = profissional.email,
        senha = profissional.senha,
        cpf = profissional.cpf,
        endereco = profissional.endereco,
        foto =  ContentFile(foto_data, name = foto.name),
        banner = ContentFile(banner_data, name = banner.name)
    )
    NovoProfissional.save()
    return {"mensagem": "profissional cadastrado"}

#Buscar todos os Profissionais
@api.get('profissional/', response=List[ProfissionalSchema])
def buscar_Profissionais(request):
    return Profissional.objects.all()

#Bucar Profissional por id
@api.get('profissional/{id}', response= ProfissionalSchema)
def buscar_prof_Id(request, id: int):
    prof = Profissional.objects.get(id=id)
    return prof

#Buscar Profissional por nome
@api.get('profissional/nome/{nome}')
def buscar_prof_nome(request, nome: str):
    try: #caso haja apenas um profissional com um nome
        prof = Profissional.objects.get(nome=nome)
        return prof
    except MultipleObjectsReturned:#caso haja mais de um profissional com o mesmo nome
        return {"existe mais de um profissional com este nome"}

#Editar todos os dados
@api.post('profissional/editar/{id}')
def editar_dados(request,id:int, nome:str, telefone:str, email: str, senha: str, cpf: str, endereco: str, fot: UploadedFile=File(None), baner: UploadedFile=File(None)):
    foto_data = fot.read()
    banner_data = baner.read()
    novoProf = get_object_or_404(Profissional, id=id)
    if novoProf:
        novoProf.nome = nome
    if novoProf:
        novoProf.telefone = telefone
    if novoProf:
        novoProf.email = email
    if novoProf:
        novoProf.senha = senha
    if novoProf:
        novoProf.cpf = cpf
    if novoProf:
        novoProf.endereco = endereco
    if novoProf:
        novoProf.foto = ContentFile(foto_data, name= fot.name)
    if novoProf:
        novoProf.banner = ContentFile(banner_data, name= baner.name)
    novoProf.save()
    return {"mensagem":"seus dados foram atualizados"}

#editar nome
@api.patch('profissional/atualizar/nome/{id}')
def atualizar_nome(request, id: int, nome: str):
    novoProf = get_object_or_404(Profissional, id=id)
    if novoProf:
       novoProf.nome = nome
    novoProf.save()
    return{"mensagem":"seu nome foi atualizado"}

@api.patch('profissional/atualizar/telefone/{id}')
def atualizar_telefone(request, id: int, telefone: str):
    novoProf = get_object_or_404(Profissional, id=id)
    if novoProf:
        novoProf.telefone = telefone
    novoProf.save()
    return{"mensagem":"seu telefone foi atualizado"}

@api.patch('profissional/atualizar/email/{id}')
def atualizar_email(request, id: int, email: str):
    novoProf = get_object_or_404(Profissional, id=id)
    if novoProf:
        novoProf.email = email
    novoProf.save()
    return {"mensagem":"seu email foi atualizado"}

@api.patch('profissional/atualizar/senha/{id}')
def atualizar_senha(request, id: int, senha: str):
    novoProf = get_object_or_404(Profissional, id=id)
    if novoProf:
        novoProf.senha = senha
    novoProf.save()
    return {"mensagem":"sua senha foi atualizada"}

@api.post('profissional/atualizar/foto/{id}')
def atualizar_foto(request, id: int, foto: UploadedFile = File(...)):
    foto_data = foto.read()
    novoProf = get_object_or_404(Profissional, id=id)
    if novoProf:
        novoProf.foto = ContentFile(foto_data, name = foto.name)
    novoProf.save()
    return {"mensagem":"sua foto foi atualizada"}

@api.post('profissional/atualizar/banner/{id}')
def atualizar_banner(request, id: int, banner: UploadedFile = File(...)):
    banner_data = banner.read()
    novoProf = get_object_or_404(Profissional, id=id)
    if novoProf:
        novoProf.banner = ContentFile(banner_data, name= banner.name)
    novoProf.save()
    return {"mensagem":"seu banner foi atualizado"}

@api.patch('profissional/atualizar/endereco/{id}')
def atualizar_endereco(request, id: int, endereco: str):
    novoProf = get_object_or_404(Profissional, id=id)
    if novoProf:
        novoProf.endereco = endereco
    novoProf.save()
    return {"mensagem":"seu endereco foi atualizado"}

@api.delete('profissional/deletar/{id}')
def deletar_profissional(request, id:int):
    novoProf = get_object_or_404(Profissional, id=id)
    novoProf.delete()
    return {"mensagem":"o profissional foi deletado"}