```mermaid
flowchart TD
  A[Página Inicial] --> B{Usuário já cadastrado?}
  B -- Sim --> C[Login]
  B -- Não --> D[Criar Cadastro]
  D --> C
  C --> E{Perfil do Usuário}
  E -- Aluno --> F[Dashboard do Aluno]
  E -- Professor --> G[Dashboard do Professor]
  E -- Coordenador --> H[Dashboard do Coordenador]
  subgraph Ações Aluno
    F --> F1[Listar Cursos Disponíveis]
    F --> F2[Inscrever-se em Turma]
    F --> F3[Acessar Trilha de Aprendizagem]
    F --> F4[Visualizar Minhas Avaliações]
  end
  subgraph Ações Professor
    G --> G1[Criar/Editar Curso]
    G --> G2[Gerenciar Turmas]
    G --> G3[Publicar Aulas]
    G --> G4[Lançar/Ver Notas]
  end
  subgraph Ações Coordenador
    H --> H1[Gerenciar Usuários]
    H --> H2[Relatórios de Desempenho]
    H --> H3[Configurar Trilhas]
    H --> H4[Auditar Conteúdo]
  end
  F1 & F2 & F3 & F4 --> I[Logout]
  G1 & G2 & G3 & G4 --> I
  H1 & H2 & H3 & H4 --> I
