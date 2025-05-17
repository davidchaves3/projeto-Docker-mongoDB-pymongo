
```markdown
# 📋 Projeto Lista de Tarefas com MongoDB + PyMongo

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-brightgreen)](https://www.mongodb.com/)
[![Build Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)]()

Aplicação simples de gerenciamento de tarefas com banco de dados MongoDB e interface de terminal em Python.

---

## 📚 Sumário

- [📋 Projeto Lista de Tarefas com MongoDB + PyMongo](#-projeto-lista-de-tarefas-com-mongodb--pymongo)
  - [📚 Sumário](#-sumário)
  - [🧠 Modelo de Dados](#-modelo-de-dados)
  - [🧱 Diagrama Simplificado](#-diagrama-simplificado)
  - [🧪 Ambiente de Execução](#-ambiente-de-execução)
  - [⚙️ Como Iniciar o Ambiente](#️-como-iniciar-o-ambiente)
  - [🛠️ Estrutura de Arquivos](#️-estrutura-de-arquivos)
  - [📌 Funcionalidades CRUD](#-funcionalidades-crud)
  - [📄 Licença](#-licença)

---

## 🧠 Modelo de Dados

Coleção: `tarefas`

| Campo         | Tipo               | Descrição                                   |
|---------------|--------------------|---------------------------------------------|
| `_id`         | ObjectId           | Identificador único gerado pelo MongoDB     |
| `titulo`      | String             | Título da tarefa                             |
| `descricao`   | String             | Descrição detalhada da tarefa                |
| `data_criacao`| Date               | Data e hora de criação da tarefa             |
| `status`      | String (enum)      | `pendente` · `em andamento` · `concluída`   |
| `tags`        | Array de Strings   | Lista de categorias                          |
| `comentarios` | Array de documentos| Lista de comentários com `autor`, `mensagem` e `data` |

---

## 🧱 Diagrama Simplificado

```markdown
tarefas
│
├── _id : ObjectId
├── titulo : string
├── descricao : string
├── data_criacao : datetime
├── status : string
├── tags : [string, ...]
└── comentarios : [
      {
        autor : string,
        mensagem : string,
        data : datetime
      }
    ]
```

---

## 🧪 Ambiente de Execução

**Banco de Dados: MongoDB + Mongo Express (via Docker)**

- MongoDB v7 com autenticação
- Mongo Express disponível em `http://localhost:8081`
- Containers definidos em `docker-compose.yml`

**Credenciais Padrão:**

| Serviço         | Usuário | Senha    |
|------------------|---------|----------|
| MongoDB          | root    | example  |
| Mongo Express UI | admin   | admin    |

---

## ⚙️ Como Iniciar o Ambiente

### 1. Subir os containers

```bash
docker-compose up -d
```

### 2. Instalar as dependências Python

```bash
pip install pymongo
```

### 3. Executar a aplicação

```bash
python main.py
```

---

## 🛠️ Estrutura de Arquivos

```
.
├── main.py            # Interface via terminal
├── crud.py            # Funções CRUD separadas
├── docker-compose.yml # Ambiente com MongoDB + Mongo Express
├── README.md          # Documentação do projeto
```

---

## 📌 Funcionalidades CRUD

✅ Criar nova tarefa  
✅ Listar tarefas por status, data ou tags  
✅ Atualizar campos de uma tarefa  
✅ Adicionar comentários  
✅ Deletar tarefa e comentários  
✅ Interface terminal interativa

---

## 📄 Licença

Este projeto é acadêmico e está licenciado sob a [MIT License](LICENSE), podendo ser utilizado e adaptado livremente para fins educacionais.

---
