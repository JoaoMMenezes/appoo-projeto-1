# appoo-projeto-1: Sistema de Gestão Educacional

Este projeto é um Sistema de Gestão Educacional desenvolvido em Python, utilizando Programação Orientada a Objetos (POO) e a biblioteca Tkinter para a interface gráfica. O sistema visa gerenciar usuários (Alunos, Professores, Coordenadores), cursos, turmas e atividades, com persistência de dados em arquivos JSON.

## Estrutura do Projeto

appoo-projeto-1/
│
├── main.py # Script principal para rodar o programa
├── README.md # Este arquivo
├── fluxograma.md # Fluxograma da aplicação
├── .gitignore # Arquivos a serem ignorados pelo Git
├── LICENSE # Licença do projeto
│
├── usuarios/
│ ├── init.py
│ ├── usuario.py # Classe base abstrata Usuario
│ ├── aluno.py # Classe Aluno (herda de Usuario)
│ ├── professor.py # Classe Professor (herda de Usuario)
│ └── coordenador.py # Classe Coordenador (herda de Usuario)
│
├── entidades/
│ ├── init.py
│ ├── curso.py # Classe Curso
│ ├── turma.py # Classe Turma
│ └── atividade.py # Classe Atividade
│
├── interface/
│ ├── init.py
│ ├── tela_login.py # Interface gráfica da tela de login
│ └── tela_menu.py # Interfaces gráficas dos menus (Aluno, Professor, Coordenador)
│
├── persistencia/
│ ├── init.py
│ └── gerenciador_dados.py # Classe para leitura e escrita de JSON
│
└── dados/
├── alunos.json # Dados dos alunos
├── professores.json # Dados dos professores
├── coordenadores.json # Dados dos coordenadores
├── turmas.json # Dados das turmas
├── cursos.json # Dados dos cursos
└── atividades.json # Dados das atividades

## Funcionalidades Principais

- **Gerenciamento de Usuários:**
  - Cadastro e autenticação de Alunos, Professores e Coordenadores.
  - Perfis de usuário distintos com diferentes permissões e dashboards.
- **Gerenciamento Acadêmico:**
  - **Alunos:** Listar cursos, inscrever-se em turmas, acessar trilhas de aprendizagem, visualizar avaliações.
  - **Professores:** Criar/editar cursos, gerenciar turmas, publicar aulas, lançar/ver notas.
  - **Coordenadores:** Gerenciar usuários, gerar relatórios de desempenho, configurar trilhas, auditar conteúdo.
- **Gerenciamento de Entidades:**
  - Criação e administração de Cursos.
  - Criação e administração de Turmas (associadas a Cursos e Professores, contendo Alunos).
  - Criação e administração de Atividades (associadas a Turmas ou Cursos).
- **Persistência de Dados:**
  - Todos os dados são salvos e carregados de arquivos JSON.
- **Interface Gráfica:**
  - Interface intuitiva desenvolvida com Tkinter, adaptada ao perfil do usuário.

## Paradigmas de POO Utilizados

- **Classes e Objetos:** Estrutura fundamental do sistema.
- **Herança:** Classes de usuários (`Aluno`, `Professor`, `Coordenador`) herdam da classe base `Usuario`.
- **Polimorfismo:** Métodos com o mesmo nome podem ter comportamentos diferentes dependendo da classe do objeto (ex: `abrir_dashboard()`).
- **Encapsulamento:** Proteção dos dados internos dos objetos, expondo interfaces controladas (getters/setters).
- **Abstração:** A classe `Usuario` é uma classe base abstrata (ABC) que define um contrato para as subclasses.
- **Composição:** Entidades complexas são formadas por outras entidades (ex: `Turma` é composta por `Aluno`s e associada a um `Curso` e `Professor`).

## Como Executar

1.  Certifique-se de ter o Python 3 instalado.
2.  Clone o repositório (ou crie os arquivos conforme a estrutura).
3.  Navegue até o diretório `appoo-projeto-1`.
4.  Execute o script principal:
    ```bash
    python main.py
    ```

## Fluxograma

Consulte o arquivo `fluxograma.md` para visualizar o fluxo da aplicação.
