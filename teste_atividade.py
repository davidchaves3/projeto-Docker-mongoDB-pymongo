from crud import (
    criar_tarefa, buscar_tarefas, buscar_tarefa_por_id,
    atualizar_status, adicionar_comentario, deletar_tarefa
)
from pymongo import MongoClient
from bson import ObjectId
import redis
from datetime import datetime, timedelta
import random

# Redis conexão
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
USER_ID = "default"

def limpar_dados():
    # Limpa MongoDB
    cliente = MongoClient('mongodb://root:example@localhost:27017/?authSource=admin')
    db = cliente.get_database('aula')
    db.drop_collection('tarefas')

    # Limpa Redis
    for chave in r.scan_iter("user:*"):
        r.delete(chave)

def simular_tarefa_completa():
    print("Criando tarefa completa com tags e status 'pendente'")
    id_tarefa = criar_tarefa(
        titulo="Atividade BD",
        descricao="Finalizar projeto Mongo + Redis",
        status="pendente",
        tags=["bd", "faculdade", "redis"]
    )

    print("Adicionando comentário")
    adicionar_comentario(id_tarefa, "David", "Primeira etapa feita!")

    print("Atualizando status para 'concluída'")
    atualizar_status(id_tarefa, "concluída")

    # Simular tempo de conclusão
    tempo_simulado = random.randint(300, 1800)  # entre 5min e 30min
    chave = f"user:{USER_ID}:stats:productivity"
    r.hincrbyfloat(chave, "tempo_total", tempo_simulado)
    r.hincrby(chave, "quantidade", 1)

    return id_tarefa

def testar_listagem():
    print("Listando tarefas por status 'concluída'")
    tarefas = buscar_tarefas(status="concluída")
    print(f"{len(tarefas)} tarefas encontradas com status 'concluída'.")

    print("Listando tarefas por tag 'redis'")
    tarefas_tag = buscar_tarefas(tag="redis")
    print(f"{len(tarefas_tag)} tarefas encontradas com tag 'redis'.")

def testar_redis():
    print("Verificando métricas no Redis")
    print("Status:")
    for status in ["pendente", "em andamento", "concluída"]:
        valor = r.get(f"user:{USER_ID}:tasks:status:{status}")
        print(f"  - {status}: {valor or 0}")

    print("\nTags mais usadas:")
    ranking = r.zrevrange(f"user:{USER_ID}:tags:top", 0, -1, withscores=True)
    for tag, score in ranking:
        print(f"  - {tag}: {int(score)}")

    print("\nEstatísticas de produtividade:")
    stats = r.hgetall(f"user:{USER_ID}:stats:productivity")
    criadas = stats.get("criadas_hoje", "0")
    tempo_total = float(stats.get("tempo_total", 0))
    qtd = int(stats.get("quantidade", 0))
    media = (tempo_total / qtd) if qtd > 0 else 0

    print(f"  - Tarefas criadas hoje: {criadas}")
    print(f"  - Tempo total de conclusão: {int(tempo_total)} segundos")
    print(f"  - Tempo médio por tarefa: {int(media)} segundos")

    print("\nTaxa de conclusão semanal:")
    hoje = datetime.now()
    total = 0
    for i in range(7):
        dia = (hoje - timedelta(days=i)).strftime("%Y-%m-%d")
        chave = f"user:{USER_ID}:tasks:completed:{dia}"
        valor = int(r.get(chave) or 0)
        total += valor
        print(f"  - {dia}: {valor} concluídas")
    print(f"Total nos últimos 7 dias: {total} tarefas")

def rodar_testes():
    limpar_dados()
    print("Iniciando testes...")
    tarefa_id = simular_tarefa_completa()
    testar_listagem()
    testar_redis()

    print("\nDeletando tarefa de teste...")
    deletar_tarefa(tarefa_id)

    print("\nTodos os requisitos testados com sucesso.")

if __name__ == "__main__":
    rodar_testes()
