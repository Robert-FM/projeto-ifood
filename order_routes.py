from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao,verificar_token
from schemas import PedidoSchema,ItemPedidoSchema
from models import Pedido,Usuario,ItemPedido

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

@order_router.get('/lista_pedidos')
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para lista os pedidos.")
    else:
        pedidos = session.query(Pedido).all()
        return {
            'pedidos': pedidos
        }
    
@order_router.post('/pedido/adicionar-item/{id_pedido}')
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao), 
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para adicionar itens a este pedido.")
    
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        'Mensagem':f'Item adicionado ao pedido com ID {pedido.id} com sucesso.',
        'pedido': pedido,
        'preco_pedido': pedido.preco
    }