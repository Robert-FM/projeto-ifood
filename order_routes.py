from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao,verificar_token
from schemas import PedidoSchema
from models import Pedido,Usuario

order_router = APIRouter(prefix='/pedidos',tags=['pedidos'],dependencies=[Depends(verificar_token)])

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

@order_router.get('/pedido/{id_pedido}')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para cancelar este pedido.")

    pedido.staus = 'Cancelado'
    session.commit()
    return {
        'Mensagem':f'Pedido com ID {pedido.id} cancelado com sucesso.',
        'pedido': pedido}