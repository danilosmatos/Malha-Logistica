from grafo import Grafo

def bfs(grafo, no1):
    visitados = []
    fila = [no1]
    visitados.append(no1)

    ordem_visita = []

    while len(fila) > 0:
        no_atual  = fila.pop(0)

        ordem_visita.append(no_atual)

        for vizinho in grafo.vizinhos[no_atual]:
            if vizinho not in visitados:
                visitados.append(vizinho)
                fila.append(vizinho)
    print(" -> ".join(ordem_visita))

    return visitados

