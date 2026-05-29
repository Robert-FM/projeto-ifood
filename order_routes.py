from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix='/pedidos',tags=['pedidos'])

@order_router.get('/')
async def pedidos():
    '''
    Essa é a rota padrão de pedidos, onde o usuário pode acessar informações 
    relacionadas aos seus pedidos.
    '''
    return {'Mensagem':'Você acessou a rotas de pedidos!'}

@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema,session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {'Mensagem':f'Pedido criado com sucesso. ID do pedido: {novo_pedido.id}.'}