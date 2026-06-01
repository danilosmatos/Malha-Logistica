import json
import os
import random


def calcular_estimativa_ram(num_vertices, num_arestas):
    """Calcula matematicamente o consumo de RAM (em bytes) das duas estruturas.

    Garante o cumprimento do RF03 (Relatório de consumo de RAM).
    """
    # Matriz: V * V * 4 bytes (considerando inteiros de 32-bits para armazenar pesos/adjacência)
    ram_matriz = num_vertices * num_vertices * 4

    # Lista: V * 8 bytes (ponteiros/referências) + A * 12 bytes (objeto nó: destino + peso + próx)
    # Multiplicado por 2 considerando uma malha logística de vias de mão dupla (não-direcionado)
    ram_lista = (num_vertices * 8) + (num_arestas * 12 * 2)

    return {
        "vertices": num_vertices,
        "arestas": num_arestas,
        "bytes_estimados_matriz": ram_matriz,
        "bytes_estimados_lista": ram_lista,
        "diferenca_bytes": abs(ram_matriz - ram_lista),
        "estrutura_mais_eficiente": "Lista de Adjacência"
        if ram_lista < ram_matriz
        else "Matriz de Adjacência",
    }


def gerar_cenario(num_encomendas, num_cidades, tipo_cenario):
    """Gera dados dinâmicos seguindo estritamente as regras de cada nível de complexidade."""
    # Anexo do Projeto 5: IDs obrigatoriamente crescentes para forçar desbalanceamento da AVL (RF02)
    encomendas = [100000 + i for i in range(num_encomendas)]

    cidades = [f"Cidade_{i}" for i in range(num_cidades)]
    rotas = []
    arestas_existentes = set()

    if tipo_cenario == "basico":
        # Conexão linear simples para validar lógica inicial
        for i in range(num_cidades - 1):
            rotas.append(
                {"origem": cidades[i], "destino": cidades[i + 1], "distancia": 10}
            )

    elif tipo_cenario == "avancado":
        # Correção do Bug de Sintaxe: Inserção manual controlada de Edge Cases
        # 1. Criação de um ciclo fechado (Cidade 0 -> 1 -> 2 -> 0)
        rotas.append({"origem": cidades[0], "destino": cidades[1], "distancia": 5})
        rotas.append({"origem": cidades[1], "destino": cidades[2], "distancia": 5})
        rotas.append({"origem": cidades[2], "destino": cidades[0], "distancia": 5})

        # 2. Dados repetidos (Mesma rota duplicada para testar tratamento de redundância)
        rotas.append({"origem": cidades[0], "destino": cidades[1], "distancia": 5})

        # 3. Componentes desconectados: Conecta o restante, deixando as últimas isoladas
        for i in range(3, num_cidades - 3):
            rotas.append(
                {"origem": cidades[i], "destino": cidades[i + 1], "distancia": 15}
            )

    elif tipo_cenario == "estresse":
        # Grafo esparso massivo (Malha logística real). Evita estouro de memória na lista.
        for i in range(num_cidades):
            # Garante que cada nó tenha de 2 a 3 conexões aleatórias
            vizinhos_alvo = random.sample(
                range(num_cidades), k=random.randint(2, 3)
            )
            for v in vizinhos_alvo:
                if i != v and (i, v) not in arestas_existentes:
                    rotas.append(
                        {
                            "origem": cidades[i],
                            "destino": cidades[v],
                            "distancia": random.randint(10, 150),
                        }
                    )
                    arestas_existentes.add((i, v))

    # RF03: Cálculo de RAM embutido nos metadados do arquivo
    relatorio_ram_teorico = calcular_estimativa_ram(num_cidades, len(rotas))

    return {
        "metadata": {
            "cenario": tipo_cenario,
            "total_encomendas": len(encomendas),
            "total_cidades": len(cidades),
            "total_rotas": len(rotas),
        },
        "encomendas": encomendas,
        "cidades": cidades,
        "rotas": rotas,
        "analise_memoria_teorica": relatorio_ram_teorico,
    }


def salvar_json(dados, nome_arquivo):
    """Salva o arquivo na pasta correta exigida pela árvore de diretórios do projeto (/data)."""
    os.makedirs("data", exist_ok=True)
    caminho = os.path.join("data", nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print(f"✔️ Arquivo '{caminho}' gerado com sucesso.")


if __name__ == "__main__":
    print("=== ENGENHARIA DE DADOS: GERADOR DE CENÁRIOS (PROJETO 5) ===")

    # 1. Cenário Básico
    salvar_json(
        gerar_cenario(num_encomendas=10, num_cidades=5, tipo_cenario="basico"),
        "input_basico.json",
    )

    # 2. Cenário Avançado (Edge cases)
    salvar_json(
        gerar_cenario(
            num_encomendas=50, num_cidades=15, tipo_cenario="avancado"
        ),
        "input_avancado.json",
    )

    # 3. Cenário de Estresse (Meta estrita do anexo: 50.000 encomendas)
    # Alocado 10.000 cidades para criar um cenário severo de comparação de matriz (400MB) vs lista (KBs)
    salvar_json(
        gerar_cenario(
            num_encomendas=50000, num_cidades=10000, tipo_cenario="estresse"
        ),
        "input_estresse.json",
    )

    print("\n[SUCESSO] Todos os arquivos foram alocados no diretório /data.")
