# 🍕 API REST para Gerenciamento de Pedidos

API REST desenvolvida com **FastAPI** para gerenciamento de usuários e pedidos, utilizando autenticação JWT, banco de dados SQLite e migrações com Alembic.

O projeto simula funcionalidades básicas de uma plataforma de delivery, permitindo o cadastro de usuários, autenticação, criação e gerenciamento de pedidos, controle de permissões e gerenciamento de itens dos pedidos.

---

# 🚀 Tecnologias Utilizadas

- Python 3.14+
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- JWT (JSON Web Token)
- Passlib (bcrypt)
- Python-Jose
- Uvicorn
- Python-Dotenv
- Pydantic

---

# 📁 Estrutura do Projeto

```text
PROJETO-IFOOD/
│
├── alembic/                 # Controle de migrações do banco de dados
│   ├── versions/            # Arquivos de migração
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── database/
│   └── banco.db             # Banco de dados SQLite
│
├── .env                     # Variáveis de ambiente
├── .gitignore
├── .python-version
├── alembic.ini              # Configuração do Alembic
│
├── auth_routes.py           # Rotas de autenticação
├── dependencies.py          # Dependências e autenticação JWT
├── main.py                  # Inicialização da aplicação FastAPI
├── models.py                # Modelos SQLAlchemy
├── order_routes.py          # Rotas de pedidos
├── schemas.py               # Schemas Pydantic
│
├── pyproject.toml           # Dependências do projeto
├── uv.lock                  # Lock das dependências
├── anotacoes.txt            # Anotações do projeto
└── README.md                # Documentação
```

> ⚠️ **Nota de Compatibilidade:** O projeto utiliza `passlib[bcrypt]==1.7.4` e `bcrypt==4.0.1`. Versões mais recentes do `bcrypt` podem apresentar incompatibilidades com o `passlib`, por isso essas versões foram fixadas no arquivo `pyproject.toml`.

---

# ⚙️ Instalação

## 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/projeto-ifood.git
```

```bash
cd projeto-ifood
```

---

## 2. Crie e ative um ambiente virtual

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Instale as dependências

Utilizando UV:

```bash
uv sync
```

ou utilizando pip:

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET-KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Descrição das variáveis:

| Variável | Descrição |
|-----------|------------|
| SECRET-KEY | Chave utilizada para assinatura dos tokens JWT |
| ALGORITHM | Algoritmo utilizado para criptografia do token |
| ACCESS_TOKEN_EXPIRE_MINUTES | Tempo de expiração do token de acesso |

---

# 🗄️ Banco de Dados

O projeto utiliza SQLite como banco de dados padrão.

## Gerar uma migração

```bash
alembic revision --autogenerate -m "initial migration"
```

## Aplicar migrações

```bash
alembic upgrade head
```

---

# ▶️ Executando a Aplicação

Inicie o servidor:

```bash
uvicorn main:app --reload
```

A aplicação ficará disponível em:

```text
http://localhost:8000
```

---

# 📖 Documentação Interativa

FastAPI gera automaticamente a documentação.

Swagger UI:

```text
http://localhost:8000/docs
```

Redoc:

```text
http://localhost:8000/redoc
```

---

# 🔑 Autenticação

A autenticação é baseada em JWT (JSON Web Token).

Fluxo:

1. Criar uma conta
2. Realizar login
3. Receber Access Token
4. Utilizar o token nas rotas protegidas

Header necessário:

```http
Authorization: Bearer seu_token
```

---

# 👤 Usuários

## Criar Conta

### Endpoint

```http
POST /auth/criar_conta
```

### Exemplo de Requisição

```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "123456",
  "ativo": true,
  "admin": false
}
```

### Resposta

```json
{
  "Mensagem": "Conta criada com sucesso!"
}
```

---

## Login

### Endpoint

```http
POST /auth/login
```

### Exemplo

```json
{
  "email": "joao@email.com",
  "senha": "123456"
}
```

### Resposta

```json
{
  "access_token": "jwt_token",
  "refresh_token": "jwt_token",
  "token_type": "Bearer"
}
```

---

## Renovar Token

### Endpoint

```http
POST /auth/refresh
```

---

# 🍕 Pedidos

Todas as rotas de pedidos exigem autenticação.

---

## Criar Pedido

### Endpoint

```http
POST /pedidos/pedido
```

### Corpo da Requisição

```json
{
  "usuario": 1
}
```

---

## Adicionar Item ao Pedido

### Endpoint

```http
POST /pedidos/pedido/adicionar-item/{id_pedido}
```

### Exemplo

```json
{
  "quantidade": 2,
  "sabor": "Calabresa",
  "tamanho": "Grande",
  "preco_unitario": 45.90
}
```

---

## Remover Item do Pedido

### Endpoint

```http
POST /pedidos/pedido/remover-item/{id_item_pedido}
```

---

## Visualizar Pedido

### Endpoint

```http
GET /pedidos/pedido/{id_pedido}
```

---

## Cancelar Pedido

### Endpoint

```http
GET /pedidos/pedido/cancelar/{id_pedido}
```

---

## Finalizar Pedido

### Endpoint

```http
GET /pedidos/pedido/finalizar/{id_pedido}
```

---

## Listar Pedidos do Usuário

### Endpoint

```http
GET /pedidos/lista_pedidos/pedidos-usuario
```

---

## Listar Todos os Pedidos

### Endpoint

```http
GET /pedidos/lista_pedidos
```

### Observação

Apenas usuários administradores possuem acesso a esta rota.

---

# 🏗️ Modelagem do Banco de Dados

## Usuário

| Campo | Tipo |
|---------|---------|
| id | Integer |
| nome | String |
| email | String |
| senha | String |
| ativo | Boolean |
| admin | Boolean |

---

## Pedido

| Campo | Tipo |
|---------|---------|
| id | Integer |
| status | String |
| usuario | Foreign Key |
| preco | Float |

---

## ItemPedido

| Campo | Tipo |
|---------|---------|
| id | Integer |
| quantidade | Integer |
| sabor | String |
| tamanho | String |
| preco_unitario | Float |
| pedido | Foreign Key |

---

# 🔒 Controle de Permissões

O sistema possui dois tipos de usuários:

## Usuário Comum

Pode:

- Criar pedidos
- Visualizar seus próprios pedidos
- Adicionar itens aos seus pedidos
- Remover itens dos seus pedidos
- Cancelar pedidos próprios
- Finalizar pedidos próprios

## Administrador

Pode:

- Visualizar todos os pedidos
- Gerenciar pedidos de qualquer usuário
- Realizar todas as operações disponíveis

---

# 📦 Dependências Principais

```toml
fastapi
sqlalchemy
alembic
uvicorn
passlib
bcrypt
python-jose
python-dotenv
python-multipart
```

---

# 🔮 Melhorias Futuras

- Testes automatizados com Pytest
- Docker e Docker Compose
- PostgreSQL
- Paginação de pedidos
- Integração com gateway de pagamento
- Cadastro de produtos
- Sistema de cupons
- Painel administrativo
- Deploy na AWS
- Deploy na Azure
- Deploy no Google Cloud

---

# 👨‍💻 Autor

**Robert Melo**

Projeto desenvolvido para estudo e prática dos conceitos de:

- FastAPI
- APIs REST
- SQLAlchemy
- JWT Authentication
- Alembic
- Arquitetura Backend em Python

---

⭐ Se este projeto foi útil para você, deixe uma estrela no repositório.
