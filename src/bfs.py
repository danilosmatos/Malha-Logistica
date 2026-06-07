def menor_caminho_bfs(grafo, origem, destino):
    """Retorna o menor caminho entre origem e destino pelo número de baldeações."""
    if origem == destino:
        return [origem]

    visitados = set()
    fila = [origem]
    anterior = {origem: None}
    inicio_fila = 0
    visitados.add(origem)

    while inicio_fila < len(fila):
        atual = fila[inicio_fila]
        inicio_fila += 1

        for vizinho in grafo.obter_vizinhos(atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                anterior[vizinho] = atual

                if vizinho == destino:
                    return reconstruir_caminho(anterior, destino)

                fila.append(vizinho)

    return []


def reconstruir_caminho(anterior, destino):
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]

    caminho.reverse()
    return caminho
