class Grafo:

    def __init__(self, nos):
        self.nos = nos
        self.vizinhos = {}
        self.indices = {}
        self.matriz = None

        for indice, no in enumerate(self.nos):
            self.vizinhos[no] = []
            self.indices[no] = indice

    def add_aresta(self, u, v):
        if u not in self.vizinhos or v not in self.vizinhos:
            raise ValueError(f"Rota inválida: {u} -> {v}")

        if v not in self.vizinhos[u]:
            self.vizinhos[u].append(v)
        if u not in self.vizinhos[v]:
            self.vizinhos[v].append(u)

    def carregar_rotas(self, rotas):
        for rota in rotas:
            self.add_aresta(rota["origem"], rota["destino"])

    def obter_vizinhos(self, no):
        return self.vizinhos.get(no, [])

    def construir_matriz(self):
        tamanho = len(self.nos)
        self.matriz = []

        for _ in range(tamanho):
            self.matriz.append([0] * tamanho)

        for origem in self.vizinhos:
            i = self.indices[origem]
            for destino in self.vizinhos[origem]:
                j = self.indices[destino]
                self.matriz[i][j] = 1

        return self.matriz

    def total_arestas_lista(self):
        total = 0
        for no in self.nos:
            total += len(self.vizinhos[no])
        return total // 2

    def listar_vizinhos(self):
        for no in self.nos:
            print(f"{no} -> {self.vizinhos[no]}")

    def total_Nos(self):
        quantidade = []
        for no in self.nos:
            quantidade.append(len(self.vizinhos[no]))
        return quantidade
