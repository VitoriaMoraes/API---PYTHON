from django.http import HttpRequest, JsonResponse
from ninja import ModelSchema, NinjaAPI, Schema
from .models import Cliente
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from ninja import Router
from typing import List
import orjson
from ninja.parser import Parser
from django.http import HttpRequest

class ORJSONParser(Parser):
    def parse_body(self, request: HttpRequest):
        return orjson.loads(request.body)

api = NinjaAPI(parser=ORJSONParser())
router_api = Router()


#Schema para ciração de usuário
class ClienteSchema(ModelSchema):
    class Config:
        model = Cliente
        model_fields = ['nome','telefone','cpf','email','senha']

#criar usuário 
@api.post('cliente', response=ClienteSchema)
def criar_cliente(request, cliente: ClienteSchema):
    cliente = (cliente.dict())
    NovoCliente = Cliente(**cliente)
    NovoCliente.save()
    return NovoCliente

#buscar
@api.get('cliente/')
def listar_todos(request):
    clientes = Cliente.objects.all()
    ListaCliente = [{'id':i.id, 'nome':i.nome, 'telefone':i.telefone, 'cpf':i.cpf, 'email':i.email, 'senha':i.senha} for i in clientes]
    return ListaCliente

#buscar por id
@api.get('cliente/{id}')
def listar_por_id(request, id: int):
    cliente = get_object_or_404(Cliente, id=id)
    return model_to_dict(cliente)

#buscar por nome
@api.get('cliente/nome/{nome}')
def listar_por_nome(request, nome: str):
    clienteNome = Cliente.objects.get(nome=nome)
    return {'mensagem':'usuario encontrado '}

#editar todos os dados 
@api.put('cliente/editar/{id}')
def editar_dados(request, id:int, nome : str, telefone: str, cpf: str, email: str, senha: str):
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

#atualizar telefone
@api.patch('cliente/atualizar/senha/{id}')
def editar_senha(request, id:int, senha :  str):
    dado = get_object_or_404(Cliente, id=id)
    if dado:
        dado.senha = senha
    dado.save()
    return {'mensagem':'sua senha foi modificada!'}

#deletar
@api.delete('cliente/deletar/{id}')
def deletar(request, id:int):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    return {'mensagem':'o cliente foi deletado'}