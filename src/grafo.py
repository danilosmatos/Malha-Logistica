class Grafo:

    def __init__(self, Nos):
        self.nos = Nos
        self.vizinhos = {}

        for no in self.nos:
            self.vizinhos[no] = []

    def add_aresta(self, u, v):
        self.vizinhos[u].append(v)
        self.vizinhos[v].append(u)

    def listar_vizinhos(self):
        for no in self.nos:
            print(f"{no} -> {self.vizinhos[no]}")

    def total_Nos(self):
        quantidade = []
        for no in self.nos:
            quantidade.append(len(self.vizinhos[no]))
        return quantidade
