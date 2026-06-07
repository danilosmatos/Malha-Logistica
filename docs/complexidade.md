# Complexidade das estruturas e algoritmos

Este projeto implementa o núcleo do Projeto 5 — Otimizador de Malha Logística.
O sistema usa Árvore AVL para organizar os IDs das encomendas, grafo para representar a malha logística e BFS para calcular rotas com o menor número de baldeações.

## Árvore AVL

A AVL armazena as encomendas pelo campo `id`.

- Inserção de uma encomenda: `O(log N)`
- Busca por ID: `O(log N)`
- Inserção de N encomendas: `O(N log N)`
- Memória: `O(N)`

O cenário de estresse insere 50.000 IDs em ordem crescente. Esse caso força rotações automáticas e demonstra a necessidade de uma árvore balanceada.

## Grafo com lista de adjacência

A lista de adjacência representa cada cidade e seus vizinhos diretos.

- Construção: `O(V + E)`
- Memória: `O(V + E)`
- Boa escolha para malhas esparsas, nas quais nem todas as cidades estão ligadas entre si.

## Grafo com matriz de adjacência

A matriz usa uma tabela `V x V`, marcando se existe rota entre duas cidades.

- Construção: `O(V²)`
- Memória: `O(V²)`
- Acesso direto a uma ligação: `O(1)`

A matriz é simples, mas consome muito mais memória quando o número de cidades cresce.

## BFS

O BFS calcula o menor caminho em número de arestas, interpretado no projeto como o menor número de baldeações.

- Tempo com lista de adjacência: `O(V + E)`
- Memória auxiliar: `O(V)`

O algoritmo usa fila manual com índice de início, evitando `pop(0)`, que teria custo `O(N)` em listas Python.
