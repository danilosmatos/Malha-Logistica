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
