import json
import os
import sys
from avl import ArvoreAVL
from bfs import menor_caminho_bfs
from grafo import Grafo
from memoria import calcular_estimativa_ram


CENARIOS_PADRAO = {
    "1": {
        "nome": "Básico",
        "input": "data/input_basico.json",
        "output": "data/output_basico.json",
        "esperado": "data/output_esperado_basico.json",
    },
    "2": {
        "nome": "Avançado",
        "input": "data/input_avancado.json",
        "output": "data/output_avancado.json",
        "esperado": "data/output_esperado_avancado.json",
    },
    "3": {
        "nome": "Estresse",
        "input": "data/input_estresse.json",
        "output": "data/output_estresse.json",
        "esperado": "data/output_esperado_estresse.json",
    },
}


def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_json(dados, caminho):
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def processar(input_path, output_path):
    dados = carregar_json(input_path)

    cidades = dados["cidades"]
    rotas = dados["rotas"]
    encomendas = dados["encomendas"]
    consultas = dados.get("consultas_rotas")

    if consultas is None:
        consultas = [encomenda["id"] for encomenda in encomendas[:50]]

    arvore = ArvoreAVL()
    arvore.carregar_encomendas(encomendas)

    grafo = Grafo(cidades)
    grafo.carregar_rotas(rotas)
    grafo.construir_matriz()

    rotas_calculadas = []
    for id_encomenda in consultas:
        encomenda = arvore.buscar(id_encomenda)

        if encomenda is None:
            rotas_calculadas.append(
                {
                    "id_encomenda": id_encomenda,
                    "encontrada": False,
                    "origem": None,
                    "destino": None,
                    "caminho": [],
                    "baldeacoes": -1,
                }
            )
            continue

        origem = encomenda["cidade_origem"]
        destino = encomenda["cidade_destino"]
        caminho = menor_caminho_bfs(grafo, origem, destino)

        rotas_calculadas.append(
            {
                "id_encomenda": id_encomenda,
                "encontrada": len(caminho) > 0,
                "origem": origem,
                "destino": destino,
                "caminho": caminho,
                "baldeacoes": len(caminho) - 1 if caminho else -1,
            }
        )

    relatorio = {
        "status": "OK",
        "cenario": dados.get("metadata", {}).get("cenario", "desconhecido"),
        "avl": {
            "total_encomendas": arvore.total_encomendas(),
            "altura": arvore.altura(),
            "primeiros_ids_em_ordem": arvore.primeiros_ids(10),
        },
        "grafo": {
            "total_cidades": len(cidades),
            "total_rotas_arquivo": len(rotas),
            "total_arestas_unicas": grafo.total_arestas_lista(),
            "matriz_construida": grafo.matriz is not None,
        },
        "rotas_calculadas": rotas_calculadas,
        "memoria": calcular_estimativa_ram(len(cidades), grafo.total_arestas_lista()),
    }

    salvar_json(relatorio, output_path)
    return relatorio


def comparar_json(caminho_a, caminho_b):
    if not os.path.exists(caminho_a) or not os.path.exists(caminho_b):
        return False

    return carregar_json(caminho_a) == carregar_json(caminho_b)


def mostrar_resumo(relatorio, output_path):
    print("\nExecução concluída.")
    print(f"Arquivo gerado: {output_path}")
    print(f"Cenário: {relatorio['cenario']}")
    print(f"Total de encomendas na AVL: {relatorio['avl']['total_encomendas']}")
    print(f"Altura da AVL: {relatorio['avl']['altura']}")
    print(f"Cidades no grafo: {relatorio['grafo']['total_cidades']}")
    print(f"Rotas calculadas por BFS: {len(relatorio['rotas_calculadas'])}")
    print(
        "Estrutura com menor consumo estimado: "
        f"{relatorio['memoria']['estrutura_mais_eficiente']}"
    )


def pedir_caminho(mensagem, caminho_padrao=None):
    if caminho_padrao:
        resposta = input(f"{mensagem} [{caminho_padrao}]: ").strip()
        return resposta if resposta else caminho_padrao

    return input(f"{mensagem}: ").strip()


def escolher_saida(cenario):
    print("\nEscolha onde salvar a saída:")
    print(f"1 - Saída comum ({cenario['output']})")
    print(f"2 - Output esperado ({cenario['esperado']})")
    print("3 - Caminho personalizado")

    opcao = input("Opção: ").strip()

    if opcao == "2":
        return cenario["esperado"]
    if opcao == "3":
        return pedir_caminho("Digite o caminho do arquivo de saída")

    return cenario["output"]


def executar_cenario(cenario):
    input_path = cenario["input"]
    output_path = escolher_saida(cenario)

    relatorio = processar(input_path, output_path)
    mostrar_resumo(relatorio, output_path)

    esperado = cenario["esperado"]
    if output_path != esperado and os.path.exists(esperado):
        if comparar_json(output_path, esperado):
            print("Resultado igual ao output esperado.")
        else:
            print("Resultado diferente do output esperado.")


def executar_personalizado():
    input_path = pedir_caminho("Digite o caminho do arquivo de entrada")
    output_path = pedir_caminho("Digite o caminho do arquivo de saída")

    relatorio = processar(input_path, output_path)
    mostrar_resumo(relatorio, output_path)

    esperado = pedir_caminho(
        "Digite um output esperado para comparar, ou pressione Enter para pular", ""
    )
    if esperado:
        if comparar_json(output_path, esperado):
            print("Resultado igual ao output esperado informado.")
        else:
            print("Resultado diferente do output esperado informado.")


def gerar_todos_outputs_esperados():
    print("\nGerando outputs esperados...")
    for chave in sorted(CENARIOS_PADRAO):
        cenario = CENARIOS_PADRAO[chave]
        relatorio = processar(cenario["input"], cenario["esperado"])
        print(
            f"{cenario['nome']}: {cenario['esperado']} "
            f"({len(relatorio['rotas_calculadas'])} rotas calculadas)"
        )
    print("Outputs esperados atualizados.")


def menu_interativo():
    while True:
        print("\n=== Otimizador de Malha Logística ===")
        print("1 - Processar input básico")
        print("2 - Processar input avançado")
        print("3 - Processar input estresse")
        print("4 - Escolher arquivos manualmente")
        print("5 - Gerar/atualizar todos os outputs esperados")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao in CENARIOS_PADRAO:
            try:
                executar_cenario(CENARIOS_PADRAO[opcao])
            except Exception as erro:
                print(f"Erro durante a execução: {erro}")
        elif opcao == "4":
            try:
                executar_personalizado()
            except Exception as erro:
                print(f"Erro durante a execução: {erro}")
        elif opcao == "5":
            try:
                gerar_todos_outputs_esperados()
            except Exception as erro:
                print(f"Erro durante a execução: {erro}")
        elif opcao == "0":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")


def main():
    if len(sys.argv) == 1:
        menu_interativo()
        return

    if len(sys.argv) == 3:
        relatorio = processar(sys.argv[1], sys.argv[2])
        mostrar_resumo(relatorio, sys.argv[2])
        return

    print("Uso:")
    print("  python src/main.py")
    print("  python src/main.py <arquivo_entrada.json> <arquivo_saida.json>")
    sys.exit(1)


if __name__ == "__main__":
    main()
