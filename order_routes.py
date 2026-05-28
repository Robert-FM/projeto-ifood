from fastapi import APIRouter

order_router = APIRouter(prefix='/pedidos',tags=['pedidos'])

@order_router.get('/')
async def pedidos():
    '''
    Essa é a rota padrão de pedidos, onde o usuário pode acessar informações 
    relacionadas aos seus pedidos.
    '''
    return {'Mensagem':'Você acessou a rotas de pedidos!'}