# Otimizador de Malha Logística

Este projeto foi desenvolvido como parte dos requisitos acadêmicos para a disciplina de Estrutura de Dados Avançado. O objetivo principal é implementar um sistema inteligente capaz de despachar encomendas otimizando rotas, organizando pacotes de forma eficiente e comparando o consumo de recursos computacionais através de estruturas de dados customizadas, **sem o uso de bibliotecas nativas** para a lógica central.

---

## Membros do Projeto
[Antônio Gabriel](https://github.com/Anton-Gabriel-code)

[Danilo Soares](https://github.com/danilosmatos)

[Eudes de Oliveira](https://github.com/eudesolv)

[Vinicius Augusto](https://github.com/Vinicius1213)

## Estruturas implementadas

- Grafo com lista de adjacência
- Grafo com matriz de adjacência
- BFS para menor número de baldeações
- Árvore AVL para organizar IDs de encomendas
- Relatório estimado de consumo de RAM entre matriz e lista

## Estrutura do repositório

```text
/src
  avl.py              Implementação da Árvore AVL
  bfs.py              Busca em Largura para menor caminho
  grafo.py            Lista e matriz de adjacência
  gerador_dados.py    Geração dos cenários de teste
  main.py             Integração geral do sistema
  memoria.py          Estimativa de RAM
/data
  input_basico.json
  input_avancado.json
  input_estresse.json
  output_esperado_basico.json
  output_esperado_avancado.json
  output_esperado_estresse.json
/docs
  complexidade.md
  prova_de_carga.md
run.sh
```

## Como gerar os dados

```bash
python src/gerador_dados.py
```

Esse comando gera os três arquivos de entrada em `/data`.

## Como executar

Para abrir o menu simples de execução:

```bash
python src/main.py
```

No menu, é possível escolher o cenário básico, avançado ou estresse, definir se a saída será comum ou se atualizará o output esperado, e também informar caminhos personalizados.

## Saída

O arquivo de saída contém:

- status da execução
- altura da AVL
- primeiros IDs em ordem
- total de cidades e rotas
- caminhos calculados por BFS
- número de baldeações
- comparação estimada de memória entre matriz e lista de adjacência
