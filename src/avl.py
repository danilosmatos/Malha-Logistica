class NoAVL:
    def __init__(self, valor, encomenda=None):
        self.valor = valor
        self.encomenda = encomenda
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def _altura(self, no):
        if no is None:
            return 0
        return no.altura

    def _fator_balanceamento(self, no):
        if no is None:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))

    def rotacionar_direita(self, y):
        x = y.esquerda
        t2 = x.direita

        x.direita = y
        y.esquerda = t2

        self._atualizar_altura(y)
        self._atualizar_altura(x)
        return x

    def rotacionar_esquerda(self, x):
        y = x.direita
        t2 = y.esquerda

        y.esquerda = x
        x.direita = t2

        self._atualizar_altura(x)
        self._atualizar_altura(y)
        return y

    def _balancear(self, no):
        self._atualizar_altura(no)
        fator = self._fator_balanceamento(no)

        if fator > 1:
            if self._fator_balanceamento(no.esquerda) < 0:
                no.esquerda = self.rotacionar_esquerda(no.esquerda)
            return self.rotacionar_direita(no)

        if fator < -1:
            if self._fator_balanceamento(no.direita) > 0:
                no.direita = self.rotacionar_direita(no.direita)
            return self.rotacionar_esquerda(no)

        return no

    def inserir(self, valor, encomenda=None):
        self.raiz = self._inserir(self.raiz, valor, encomenda)

    def _inserir(self, no, valor, encomenda):
        if no is None:
            return NoAVL(valor, encomenda)

        if valor < no.valor:
            no.esquerda = self._inserir(no.esquerda, valor, encomenda)
        elif valor > no.valor:
            no.direita = self._inserir(no.direita, valor, encomenda)
        else:
            no.encomenda = encomenda
            return no

        return self._balancear(no)

    def carregar_encomendas(self, encomendas):
        for encomenda in encomendas:
            self.inserir(encomenda["id"], encomenda)

    def buscar(self, valor):
        no = self._buscar(valor)
        if no is None:
            return None
        return self._formatar_no(no)

    def _buscar(self, valor):
        atual = self.raiz
        while atual is not None:
            if valor == atual.valor:
                return atual
            if valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def remover(self, valor):
        existe = self._buscar(valor) is not None
        self.raiz = self._remover(self.raiz, valor)
        return existe

    def _remover(self, no, valor):
        if no is None:
            return None

        if valor < no.valor:
            no.esquerda = self._remover(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._remover(no.direita, valor)
        else:
            if no.esquerda is None:
                return no.direita
            if no.direita is None:
                return no.esquerda

            sucessor = self._minimo(no.direita)
            no.valor = sucessor.valor
            no.encomenda = sucessor.encomenda
            no.direita = self._remover(no.direita, sucessor.valor)

        return self._balancear(no)

    def _minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def listar(self):
        resultado = []
        self._inorder(self.raiz, resultado)
        return resultado

    def _inorder(self, no, resultado):
        if no is None:
            return
        self._inorder(no.esquerda, resultado)
        resultado.append(no.valor)
        self._inorder(no.direita, resultado)

    def recomendar(self, valor_referencia):
        no = self._recomendar(self.raiz, valor_referencia)
        if no is None:
            return None
        resultado = dict(self._formatar_no(no))
        resultado["distancia"] = abs(no.valor - valor_referencia)
        return resultado

    def _recomendar(self, no, valor_referencia, melhor=None):
        if no is None:
            return melhor

        dist_atual = abs(no.valor - valor_referencia)
        if melhor is None:
            melhor = no
        else:
            dist_melhor = abs(melhor.valor - valor_referencia)
            if dist_atual < dist_melhor or (
                dist_atual == dist_melhor and no.valor < melhor.valor
            ):
                melhor = no

        if valor_referencia < no.valor:
            return self._recomendar(no.esquerda, valor_referencia, melhor)
        if valor_referencia > no.valor:
            return self._recomendar(no.direita, valor_referencia, melhor)
        return no

    def _formatar_no(self, no):
        if no.encomenda is not None:
            return no.encomenda
        return {"id": no.valor}

    def vazia(self):
        return self.raiz is None

    def tamanho(self):
        return len(self.listar())


    def altura(self):
        return self._altura(self.raiz)

    def primeiros_ids(self, quantidade):
        resultado = []
        self._coletar_primeiros(self.raiz, resultado, quantidade)
        return resultado

    def _coletar_primeiros(self, no, resultado, quantidade):
        if no is None or len(resultado) >= quantidade:
            return
        self._coletar_primeiros(no.esquerda, resultado, quantidade)
        if len(resultado) < quantidade:
            resultado.append(no.valor)
        self._coletar_primeiros(no.direita, resultado, quantidade)

    def total_encomendas(self):
        return self.tamanho()

    def imprimir(self):
        ids = self.listar()
        print(" -> ".join(str(i) for i in ids))
        return ids
