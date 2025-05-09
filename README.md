# Análise Projeto e Programação Orientada a Objetos

## Projeto 1 – Sistema de Gestão Educacional

O projeto propõe o desenvolvimento de um **sistema educacional orientado a objetos**, implementado em **Python**, com foco na gestão acadêmica de uma instituição. O sistema será estruturado com base em princípios sólidos da **Programação Orientada a Objetos (POO)** e utilizará persistência de dados em arquivos locais.

### Objetivo

Desenvolver uma aplicação modular capaz de gerenciar usuários, cursos, turmas, atividades e desempenho de alunos, respeitando as permissões e responsabilidades de cada tipo de usuário.

### Funcionalidades Principais

- **Cadastro, login e controle de acesso** com perfis distintos: `Aluno`, `Professor` e `Coordenador`, cada um com permissões específicas.
- **Gerenciamento de cursos, turmas, lições e desafios**, com vinculação a professores e acompanhamento do progresso dos alunos.
- **Lançamento e registro de notas** por professores, com histórico individual de desempenho.
- **Interface gráfica amigável**, com menus personalizados conforme o tipo de usuário.
- **Persistência de dados** via arquivos JSON, garantindo armazenamento entre execuções.
- **Tratamento de exceções** para falhas comuns, como login inválido e controle de lotação de turmas.

### Arquitetura e Técnicas Utilizadas

- **Programação Orientada a Objetos**, com:
  - **Herança** para especialização dos tipos de usuários.
  - **Polimorfismo** para permitir comportamentos distintos entre perfis.
  - **Classes abstratas** para padronizar a estrutura base dos usuários.
  - **Composição** para modelar relacionamentos entre cursos, turmas e atividades.
- **Modularização em múltiplos arquivos `.py`**, organizados por domínio lógico (ex: `usuario.py`, `curso.py`, `turma.py`, etc.).
