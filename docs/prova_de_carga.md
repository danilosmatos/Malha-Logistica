# Prova de carga

O gerador de dados cria três cenários em JSON.

## Cenário básico

Usado para validar a lógica central:

- 10 encomendas
- 5 cidades
- malha linear simples
- todas as encomendas são consultadas

## Cenário avançado

Usado para validar casos especiais:

- ciclo entre cidades
- rota duplicada
- cidades desconectadas
- rotas impossíveis para algumas encomendas

## Cenário de estresse

Usado para validar a volumetria exigida pelo Projeto 5:

- 50.000 encomendas
- IDs em ordem crescente
- 1.000 cidades
- grafo esparso com rotas aleatórias e conectividade mínima
- 100 consultas de rota para manter o output legível

A exigência do anexo é testar 50.000 IDs de encomendas. O número de cidades foi mantido em 1.000 para permitir a construção da matriz de adjacência sem tornar o programa inviável em computadores comuns.

## Saída esperada

Os arquivos `output_esperado_*.json` são gerados pelo próprio `main.py` a partir dos arquivos de entrada. Eles servem como gabarito aberto e determinístico para comparação.
