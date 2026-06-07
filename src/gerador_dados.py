import json
import os
import random

# Seed fixa para determinismo
SEED_PADRAO = 42


def gerar_cenario(num_encomendas, num_cidades, tipo_cenario, total_consultas=20):
    """Gera os dados de entrada do Projeto 5.
    cidades = [f"Cidade_{i}" for i in range(num_cidades)]
    rotas = []
    arestas_existentes = set()
    # Correção Danilo; Essencialmente mudando o append simples para uma função que checa se a rota é inválida; 
    def adicionar_rota(origem, destino, distancia):
        if origem == destino:
            return
        chave = tuple(sorted((origem, destino)))
        rotas.append({"origem": origem, "destino": destino, "distancia": distancia})
        arestas_existentes.add(chave)

    if tipo_cenario == "basico":
        # Conexão linear simples para validar a lógica central do BFS.
        for i in range(num_cidades - 1):
            adicionar_rota(cidades[i], cidades[i + 1], 10)

    elif tipo_cenario == "avancado":
        # Ciclo: Cidade_0 -> Cidade_1 -> Cidade_2 -> Cidade_0.
        adicionar_rota(cidades[0], cidades[1], 5)
        adicionar_rota(cidades[1], cidades[2], 5)
        adicionar_rota(cidades[2], cidades[0], 5)

        # Rota duplicada proposital para validar tratamento de dados repetidos.
        rotas.append({"origem": cidades[0], "destino": cidades[1], "distancia": 5})

        # Componente principal conectado até a antepenúltima cidade.
        # As duas últimas cidades ficam isoladas para testar rotas impossíveis.
        for i in range(2, num_cidades - 3):
            adicionar_rota(cidades[i], cidades[i + 1], 15)

    elif tipo_cenario == "estresse":
        # Garante conectividade mínima com uma linha principal.
        for i in range(num_cidades - 1):
            adicionar_rota(cidades[i], cidades[i + 1], random.randint(10, 80))

        # Adiciona atalhos aleatórios para simular uma malha esparsa.
        tentativas = num_cidades * 3
        for _ in range(tentativas):
            origem, destino = random.sample(cidades, k=2)
            chave = tuple(sorted((origem, destino)))
            if chave not in arestas_existentes:
                adicionar_rota(origem, destino, random.randint(10, 150))

    else:
        raise ValueError(f"Cenário desconhecido: {tipo_cenario}")

    encomendas = []

    # Casos controlados no avançado para garantir ciclo, duplicata e desconexão.
    if tipo_cenario == "avancado" and num_encomendas >= 3:
        encomendas.extend(
            [
                {
                    "id": 100000,
                    "cidade_origem": cidades[0],
                    "cidade_destino": cidades[2],
                },
                {
                    "id": 100001,
                    "cidade_origem": cidades[0],
                    "cidade_destino": cidades[1],
                },
                {
                    "id": 100002,
                    "cidade_origem": cidades[0],
                    "cidade_destino": cidades[-1],
                },
            ]
        )

    inicio = len(encomendas)
    for i in range(inicio, num_encomendas):
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

    consultas_rotas = [encomenda["id"] for encomenda in encomendas[:total_consultas]]

    return {
        "metadata": {
            "cenario": tipo_cenario,
            "seed": SEED_PADRAO,
            "total_encomendas": len(encomendas),
            "total_cidades": len(cidades),
            "total_rotas": len(rotas),
            "total_consultas": len(consultas_rotas),
            "grafo_direcionado": False,
        },
        "cidades": cidades,
        "rotas": rotas,
        "encomendas": encomendas,
        "consultas_rotas": consultas_rotas,
    }


def salvar_json(dados, nome_arquivo):
    """Salva o arquivo estruturado no diretório /data."""
    os.makedirs("data", exist_ok=True)
    caminho = os.path.join("data", nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    print(f"Arquivo gerado: {caminho}")


if __name__ == "__main__":
    random.seed(SEED_PADRAO)

    print("=== Gerador de dados - Projeto 5: Malha Logística ===")

    salvar_json(
        gerar_cenario(
            num_encomendas=10,
            num_cidades=5,
            tipo_cenario="basico",
            total_consultas=10,
        ),
        "input_basico.json",
    )

    salvar_json(
        gerar_cenario(
            num_encomendas=50,
            num_cidades=15,
            tipo_cenario="avancado",
            total_consultas=20,
        ),
        "input_avancado.json",
    )

    salvar_json(
        gerar_cenario(
            num_encomendas=50000,
            num_cidades=1000,
            tipo_cenario="estresse",
            total_consultas=100,
        ),
        "input_estresse.json",
    )

    print("Todos os arquivos foram gerados em /data.")
