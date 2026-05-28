from fastapi import APIRouter, Depends
from models import Usuario,db
from dependencies import pegar_sessao

auth_router = APIRouter(prefix='/auth',tags=['auth'])

@auth_router.get('/')
async def home():
    '''
    Essa é a rota padrão de autenticação, onde o usuário pode enviar suas credenciais 
    para obter um token de acesso.
    '''
    return {'Mensagem': 'Você acessou a rota padrão de autenticação!','autenticado':False}

@auth_router.post('/criar_conta')
async def criar_conta(email:str,senha:str,nome:str,session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return {'Mensagem':'Email já cadastrado!'}
    else:
        novo_usuario = Usuario(nome,email,senha)
        session.add(novo_usuario)
        session.commit()
        return {'Mensagem':'Conta criada com sucesso!'}