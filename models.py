from sqlalchemy import create_engine,Column, Integer, String, Boolean, ForeignKey,Float
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


#cria a conexão do seu banco de dados
db = create_engine('sqlite:///database/banco.db')

#cria a base do banco de dados
Base = declarative_base()

#cria as classes/tabelas do banco de dados
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('id',Integer,primary_key=True,autoincrement=True)
    nome = Column('nome',String(100))
    email = Column('email',String(50), nullable=False)
    senha = Column('senha',String(50))
    ativo = Column('ativo',Boolean)
    admin = Column('admin',Boolean,default=False)

    def __init__(self,nome,email,senha,ativo=True,admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = 'pedidos'

    #STAUS_PEDIDO = [
    #    ('Pendente','Pendente'),
    #    ('Cancelado','Cancelado'),
    #    ('Finalizado','Finalizado')
    #]

    id = Column('id',Integer,primary_key=True,autoincrement=True)
    staus = Column('status',String(20)) #pendente, cancelado, finalizado
    usuario = Column('usuario',ForeignKey('usuarios.id'))
    preco = Column('preco',Float)
    #itens =

    def __init__(self,usuario,status='Pendente',preco=0.0):
        self.usuario = usuario
        self.staus = status
        self.preco = preco

class ItemPedido(Base):
    __tablename__ = 'itens_pedido'
    
    id = Column('id',Integer,primary_key=True,autoincrement=True)
    quantidade = Column('quantidade',Integer)
    sabor = Column('sabor',String(50))
    tamanho = Column('tamanho',String(20))
    preco_unitario = Column('preco_unitario',Float)
    pedido = Column('pedido',ForeignKey('pedidos.id'))

    def __init__(self,quantidade,sabor,tamanho,preco_unitario,pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

#executa a criação do banco de dados
