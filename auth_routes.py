from fastapi import APIRouter, Depends, HTTPException
from models import Usuario,db
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix='/auth',tags=['auth'])

@auth_router.get('/')
async def home():
    '''
    Essa é a rota padrão de autenticação, onde o usuário pode enviar suas credenciais 
    para obter um token de acesso.
    '''
    return {'Mensagem': 'Você acessou a rota padrão de autenticação!','autenticado':False}

@auth_router.post('/criar_conta')
async def criar_conta(usuario_schemas: UsuarioSchema,session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schemas.email).first()
    if usuario:
        raise HTTPException(status_code=400,detail='E-mail já cadastrado!')
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schemas.senha)
        novo_usuario = Usuario(usuario_schemas.nome,usuario_schemas.email,senha_criptografada,
                               usuario_schemas.ativo,usuario_schemas.admin)
        session.add(novo_usuario)
        session.commit()
        return {'Mensagem':f'Conta criada com sucesso {usuario_schemas.email}!'} 