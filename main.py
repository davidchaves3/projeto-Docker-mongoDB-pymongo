from crud import (
    criar_tarefa, buscar_tarefas, buscar_tarefa_por_id,
    atualizar_tarefa, atualizar_status, adicionar_comentario,
    deletar_tarefa
)
from datetime import datetime
from metricas import r, USER_ID, obter_conclusao_semanal

def mostrar_menu():
    print("\n=== MENU TAREFAS ===")
    print("1 - Criar tarefa")
    print("2 - Listar tarefas")
    print("3 - Atualizar tarefa")
    print("4 - Atualizar status")
    print("5 - Adicionar comentário")
    print("6 - Deletar tarefa")
    print("7 - Ver métricas de produtividade") 
    print("0 - Sair")

def input_tags():
    tags = input("Tags (separadas por vírgula): ").strip().split(",")
    return [t.strip() for t in tags if t.strip()]

def criar():
    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()
    status = input("Status (pendente, em andamento, concluída): ").strip().lower()
    tags = input_tags()
    id_criada = criar_tarefa(titulo, descricao, status, tags)
    print(f"Tarefa criada com ID: {id_criada}")

def listar():
    status = input("Filtrar por status (ou Enter para todos): ").strip().lower() or None
    tag = input("Filtrar por tag (ou Enter para todos): ").strip() or None
    tarefas = buscar_tarefas(status=status if status else None, tag=tag if tag else None)
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    for t in tarefas:
        print(f"\nID: {t['_id']}")
        print(f"Título: {t['titulo']}")
        print(f"Descrição: {t['descricao']}")
        print(f"Status: {t['status']}")
        print(f"Tags: {', '.join(t['tags'])}")
        print(f"Criado em: {t['data_criacao']}")
        print(f"Comentários: {len(t.get('comentarios', []))}")

def ver_metricas():
    print("\n=== MÉTRICAS DE PRODUTIVIDADE ===\n")
    print("Tarefas por status:")
    for status in ["pendente", "em andamento", "concluída"]:
        chave = f"user:{USER_ID}:tasks:status:{status}"
        valor = r.get(chave)
        print(f"  - {status}: {valor or 0}")

    print("\nTags mais usadas:")
    ranking = r.zrevrange(f"user:{USER_ID}:tags:top", 0, -1, withscores=True)
    if ranking:
        for tag, score in ranking:
            print(f"  - {tag}: {int(score)}")
    else:
        print("  (Nenhuma tag registrada ainda)")

    print("\nProdutividade diária:")
    stats = r.hgetall(f"user:{USER_ID}:stats:productivity")
    if stats:
        criadas = stats.get("criadas_hoje", "0")
        tempo_total = float(stats.get("tempo_total", "0"))
        qtd = int(stats.get("quantidade", "0"))
        media = (tempo_total / qtd) if qtd > 0 else 0

        print(f"  - Tarefas criadas hoje: {criadas}")
        print(f"  - Tempo total de conclusão: {int(tempo_total)} segundos")
        print(f"  - Tempo médio por tarefa: {int(media)} segundos")
    else:
        print("  (Nenhuma estatística registrada ainda)")
    print("\n🔸 Taxa de conclusão semanal (últimos 7 dias):")
    total_semanal, dias = obter_conclusao_semanal()
    print(f"  - Total: {total_semanal} tarefas concluídas")
    for dia, qtd in dias:
        print(f"    {dia}: {qtd}")



def atualizar():
    id_str = input("ID da tarefa para atualizar: ").strip()
    print("Deixe em branco para não alterar o campo.")
    titulo = input("Novo título: ").strip() or None
    descricao = input("Nova descrição: ").strip() or None
    status = input("Novo status (pendente, em andamento, concluída): ").strip().lower() or None
    tags_input = input("Novas tags (separadas por vírgula): ").strip()
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else None

    modificados = atualizar_tarefa(id_str, titulo, descricao, status, tags)
    if modificados:
        print("Tarefa atualizada com sucesso.")
    else:
        print("Nenhuma tarefa foi atualizada. Verifique o ID.")

def atualizar_status_menu():
    id_str = input("ID da tarefa para atualizar o status: ").strip()
    novo_status = input("Novo status (pendente, em andamento, concluída): ").strip().lower()
    modificados = atualizar_status(id_str, novo_status)
    if modificados:
        print("Status atualizado com sucesso.")
    else:
        print("Falha ao atualizar status. Verifique o ID.")

def adicionar_comentario_menu():
    id_str = input("ID da tarefa para adicionar comentário: ").strip()
    autor = input("Autor do comentário: ").strip()
    mensagem = input("Mensagem do comentário: ").strip()
    modificados = adicionar_comentario(id_str, autor, mensagem)
    if modificados:
        print("Comentário adicionado com sucesso.")
    else:
        print("Falha ao adicionar comentário. Verifique o ID.")

def deletar():
    id_str = input("ID da tarefa para deletar: ").strip()
    confirm = input(f"Confirma deletar a tarefa {id_str}? (s/n): ").strip().lower()
    if confirm == 's':
        deletados = deletar_tarefa(id_str)
        if deletados:
            print("Tarefa deletada com sucesso.")
        else:
            print("Falha ao deletar. Verifique o ID.")
    else:
        print("Operação cancelada.")

def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == '1':
            criar()
        elif opcao == '2':
            listar()
        elif opcao == '3':
            atualizar()
        elif opcao == '4':
            atualizar_status_menu()
        elif opcao == '5':
            adicionar_comentario_menu()
        elif opcao == '6':
            deletar()
        elif opcao == '7':
            ver_metricas()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
