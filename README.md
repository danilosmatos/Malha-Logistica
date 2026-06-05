# Otimizador de Malha Logística 📦🚚

Este projeto foi desenvolvido como parte dos requisitos acadêmicos para a disciplina de Estrutura de Dados. O objetivo principal é implementar um sistema inteligente capaz de despachar encomendas otimizando rotas, organizando pacotes de forma eficiente e comparando o consumo de recursos computacionais através de estruturas de dados customizadas, **sem o uso de bibliotecas nativas** para a lógica central.

---

## 👥 Membros do Projeto
[Antônio Gabriel]((https://github.com/Anton-Gabriel-code))
[Danilo Soares]((https://github.com/danilosmatos))
[Eudes de Oliveira]((https://github.com/eudesolv))
[Vinicius Augusto]((https://github.com/Vinicius1213))

---

## 📂 Estrutura do Repositório

Seguindo o padrão obrigatório estabelecido, o projeto está organizado da seguinte forma:

```text
├── /src              # Código-fonte do projeto e implementação das estruturas
│   ├── grafo.py      # Representação do grafo (Lista de Adjacência e Matriz)
│   ├── bfs.py        # Algoritmo de Busca em Largura customizado
│   └── avl.py        # Implementação da Árvore AVL para IDs de encomendas
├── /data             # Arquivos de entrada e saída (Testes abertos e gabaritos)
│   ├── input_basico.json
│   ├── input_avancado.json
│   └── input_estresse.json
├── /docs             # Documentação técnica e justificativas de complexidade
└── README.md         # Instruções de compilação, execução e visão geral
