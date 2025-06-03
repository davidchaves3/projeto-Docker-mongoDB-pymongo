from metricas import contar_status, contar_conclusao_diaria, contar_tag, registrar_criacao_tarefa,obter_conclusao_semanal
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Conexão MongoDB
cliente = MongoClient('mongodb://root:example@localhost:27017/?authSource=admin')
db = cliente.get_database('aula')
tarefas = db.get_collection('tarefas')

# --- CREATE ---
def criar_tarefa(titulo, descricao, status, tags, comentarios=[]):
    tarefa = {
        "titulo": titulo,
        "descricao": descricao,
        "data_criacao": datetime.now(),
        "status": status,
        "tags": tags,
        "comentarios": comentarios
    }
    resultado = tarefas.insert_one(tarefa)
    registrar_criacao_tarefa()
    contar_status(status)
    for tag in tags:
        contar_tag(tag)

    return str(resultado.inserted_id)

# --- READ ---
def buscar_tarefas(status=None, tag=None, data_minima=None):
    filtro = {}
    if status:
        filtro["status"] = status
    if tag:
        filtro["tags"] = tag
    if data_minima:
        filtro["data_criacao"] = {"$gte": data_minima}

    resultados = tarefas.find(filtro)
    return list(resultados)

def buscar_tarefa_por_id(id_str):
    try:
        _id = ObjectId(id_str)
    except Exception as e:
        return None
    return tarefas.find_one({"_id": _id})

# --- UPDATE ---
def atualizar_tarefa(id_str, titulo=None, descricao=None, status=None, tags=None, comentarios=None):
    try:
        _id = ObjectId(id_str)
    except Exception as e:
        return 0

    atualizacao = {}
    if titulo is not None:
        atualizacao["titulo"] = titulo
    if descricao is not None:
        atualizacao["descricao"] = descricao
    if status is not None:
        atualizacao["status"] = status
    if tags is not None:
        atualizacao["tags"] = tags
    if comentarios is not None:
        atualizacao["comentarios"] = comentarios

    if not atualizacao:
        return 0  # Nada para atualizar
    if status == "concluída":
        contar_conclusao_diaria()

    resultado = tarefas.update_one({"_id": _id}, {"$set": atualizacao})
    return resultado.modified_count

# Atualizar status específico
def atualizar_status(id_str, novo_status):
    return atualizar_tarefa(id_str, status=novo_status)

# Adicionar comentário (append no array)
def adicionar_comentario(id_str, autor, mensagem):
    try:
        _id = ObjectId(id_str)
    except Exception:
        return 0

    comentario = {
        "autor": autor,
        "mensagem": mensagem,
        "data": datetime.now()
    }
    resultado = tarefas.update_one({"_id": _id}, {"$push": {"comentarios": comentario}})
    return resultado.modified_count

# --- DELETE ---
def deletar_tarefa(id_str):
    # Como os comentários estão embutidos na tarefa, deletar a tarefa apaga os comentários junto.
    try:
        _id = ObjectId(id_str)
    except Exception:
        return 0
    resultado = tarefas.delete_one({"_id": _id})
    return resultado.deleted_count
