import json
import os
import random


def gerar_cenario(num_encomendas, num_cidades, tipo_cenario):
    """Gera dados dinâmicos vinculando encomendas e rotas sem análise de memória."""
    # 1. Gerar as cidades do cenário
    cidades = [f"Cidade_{i}" for i in range(num_cidades)]
    rotas = []
    

    # 2. Construir as rotas com base no tipo de cenário (Estrutura do Grafo)
    if tipo_cenario == "basico":
        # Conexão linear simples para validar lógica inicial (BFS)
        for i in range(num_cidades - 1):
            rotas.append(
                {"origem": cidades[i], "destino": cidades[i + 1], "distancia": 10}
            )

    elif tipo_cenario == "avancado":
        # Inserção de Edge Cases (Ciclos, duplicados e nós isolados)
        # Ciclo fechado (Cidade 0 -> 1 -> 2 -> 0)
        rotas.append({"origem": cidades, "destino": cidades, "distancia": 5})
        rotas.append({"origem": cidades, "destino": cidades, "distancia": 5})
        rotas.append({"origem": cidades, "destino": cidades, "distancia": 5})

        # Rota duplicada (Dados repetidos)
        rotas.append({"origem": cidades, "destino": cidades, "distancia": 5})

        # Componentes desconectados: conecta até a antepenúltima cidade, isolando as últimas
        for i in range(2, num_cidades - 3):
            rotas.append(
                {"origem": cidades[i], "destino": cidades[i + 1], "distancia": 15}
            )

    elif tipo_cenario == "estresse":
        # Grafo esparso massivo simulando uma malha logística real
        arestas_existentes = set()
        
        for i in range(num_cidades):
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

    # 3. Gerar as encomendas vinculando-as a cidades reais de origem e destino
    encomendas = []
    for i in range(num_encomendas):
        # IDs crescentes para forçar pior caso/rotações automáticas na Árvore AVL
        id_encomenda = 100000 + i

        # Sorteia origem e destino garantindo que sejam cidades diferentes
        origem_enc, destino_enc = random.sample(cidades, k=2)

        encomendas.append(
            {
                "id": id_encomenda,
                "cidade_origem": origem_enc,
                "cidade_destino": destino_enc,
            }
        )

    return {
        "metadata": {
            "cenario": tipo_cenario,
            "total_encomendas": len(encomendas),
            "total_cidades": len(cidades),
            "total_rotas": len(rotas),
        },
        "cidades": cidades,
        "rotas": rotas,
        "encomendas": encomendas,
    }


def salvar_json(dados, nome_arquivo):
    """Salva o arquivo final estruturado no diretório /data."""
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

    # 2. Cenário Avançado (Foco em Edge Cases)
    salvar_json(
        gerar_cenario(
            num_encomendas=50, num_cidades=15, tipo_cenario="avancado"
        ),
        "input_avancado.json",
    )

    # 3. Cenário de Estresse (Meta estrita do anexo: 50.000 encomendas)
    salvar_json(
        gerar_cenario(
            num_encomendas=50000, num_cidades=10000, tipo_cenario="estresse"
        ),
        "input_estresse.json",
    )

    print("\n[SUCESSO] Todos os arquivos foram gerados no diretório /data.")
