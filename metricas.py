import redis
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
USER_ID = "default"

def contar_status(status):
    chave = f"user:{USER_ID}:tasks:status:{status}"
    r.incr(chave)

def contar_conclusao_diaria():
    hoje = datetime.now().strftime("%Y-%m-%d")
    chave = f"user:{USER_ID}:tasks:completed:{hoje}"
    r.incr(chave)

def contar_tag(tag):
    chave = f"user:{USER_ID}:tags:top"
    r.zincrby(chave, 1, tag)

def registrar_criacao_tarefa():
    chave = f"user:{USER_ID}:stats:productivity"
    r.hincrby(chave, "criadas_hoje", 1)
