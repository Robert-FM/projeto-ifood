from fastapi import APIRouter, Depends, HTTPException
from models import Usuario,db
from dependencies import pegar_sessao
from main import bcrypt_context,SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
from schemas import LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta,timezone

auth_router = APIRouter(prefix='/auth',tags=['auth'])

def criar_token(id_usuario: int,duracao_token: int = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token 

    dict_info = {'sub': str(id_usuario),'exp': data_expiracao}
    
    jwt_codificado = jwt.encode(dict_info,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_codificado

def verificar_token(token: str,session: Session = Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.id == 1).first()
    return usuario

def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False
    return usuario

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
        novo_usuario = Usuario(usuario_schemas.nome,
                               usuario_schemas.email,
                               senha_criptografada,
                               usuario_schemas.ativo,
                               usuario_schemas.admin)
        session.add(novo_usuario)
        session.commit()
        return {'Mensagem':f'Conta criada com sucesso {usuario_schemas.email}!'} 
    
@auth_router.post('/login')
async def login(login_schema: LoginSchema,session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400,detail='E-mail ou senha incorretos!')
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id,duracao_token=timedelta(days=7))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }
    
@auth_router.post('/refresh')
async def use_refresh_token(token):
    usuario = verificar_token(token)
    access_token = criar_token(usuario.id)
    return {
            'access_token': access_token,
            'token_type': 'Bearer'
        }