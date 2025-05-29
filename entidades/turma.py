# entidades/turma.py
from typing import List, Optional

class Turma:
    """
    Representa uma turma específica de um curso.

    Atributos:
        id_turma (str): Identificador único da turma.
        id_curso (str): ID do curso ao qual esta turma pertence.
        id_professor (Optional[str]): ID do professor responsável pela turma.
        nome_turma (str): Nome ou código da turma (ex: "2024-A").
        max_alunos (int): Número máximo de alunos na turma.
        lista_id_alunos (list[str]): Lista de IDs dos alunos matriculados na turma.
        lista_id_atividades (list[str]): Lista de IDs das atividades associadas a esta turma.
    """

    def __init__(self, id_turma: str, id_curso: str, nome_turma: str, max_alunos: int, id_professor: Optional[str] = None):
        """
        Construtor da classe Turma.

        Args:
            id_turma (str): ID da turma.
            id_curso (str): ID do curso associado.
            nome_turma (str): Nome/código da turma.
            max_alunos (int): Capacidade máxima de alunos.
            id_professor (Optional[str]): ID do professor (pode ser None inicialmente).
        """
        if not all([id_turma, id_curso, nome_turma]):
            raise ValueError("ID da turma, ID do curso e nome da turma são obrigatórios.")
        if not isinstance(max_alunos, int) or max_alunos <= 0:
            raise ValueError("Número máximo de alunos deve ser um inteiro positivo.")

        self.id_turma = id_turma
        self.id_curso = id_curso
        self.id_professor = id_professor
        self.nome_turma = nome_turma
        self.max_alunos = max_alunos
        self.lista_id_alunos: List[str] = []
        self.lista_id_atividades: List[str] = []

    def adicionar_aluno(self, id_aluno: str) -> bool:
        """
        Adiciona um aluno à turma, se houver vaga.

        Args:
            id_aluno (str): ID do aluno a ser adicionado.

        Returns:
            bool: True se o aluno foi adicionado, False caso contrário (turma cheia ou aluno já inscrito).
        """
        if len(self.lista_id_alunos) < self.max_alunos:
            if id_aluno not in self.lista_id_alunos:
                self.lista_id_alunos.append(id_aluno)
                return True
            else:
                print(f"Aluno {id_aluno} já está na turma {self.id_turma}.")
                return False
        else:
            print(f"Turma {self.id_turma} está cheia. Não foi possível adicionar o aluno {id_aluno}.")
            return False

    def remover_aluno(self, id_aluno: str):
        """Remove um aluno da turma."""
        if id_aluno in self.lista_id_alunos:
            self.lista_id_alunos.remove(id_aluno)

    def definir_professor(self, id_professor: str):
        """Define ou altera o professor da turma."""
        self.id_professor = id_professor

    def adicionar_atividade(self, id_atividade: str):
        """Adiciona o ID de uma atividade à lista de atividades da turma."""
        if id_atividade not in self.lista_id_atividades:
            self.lista_id_atividades.append(id_atividade)

    def remover_atividade(self, id_atividade: str):
        """Remove o ID de uma atividade da lista de atividades da turma."""
        if id_atividade in self.lista_id_atividades:
            self.lista_id_atividades.remove(id_atividade)

    def to_dict(self) -> dict:
        """
        Converte o objeto Turma em um dicionário para serialização.

        Returns:
            dict: Dicionário representando a turma.
        """
        return {
            "id_turma": self.id_turma,
            "id_curso": self.id_curso,
            "id_professor": self.id_professor,
            "nome_turma": self.nome_turma,
            "max_alunos": self.max_alunos,
            "lista_id_alunos": self.lista_id_alunos,
            "lista_id_atividades": self.lista_id_atividades
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria um objeto Turma a partir de um dicionário.

        Args:
            data (dict): Dicionário com os dados da turma.

        Returns:
            Turma: Uma instância da classe Turma.
        """
        turma = cls(
            id_turma=data["id_turma"],
            id_curso=data["id_curso"],
            nome_turma=data["nome_turma"],
            max_alunos=data["max_alunos"],
            id_professor=data.get("id_professor") # .get para lidar com Optional
        )
        turma.lista_id_alunos = data.get("lista_id_alunos", [])
        turma.lista_id_atividades = data.get("lista_id_atividades", [])
        return turma

    def __str__(self) -> str:
        return f"Turma: {self.nome_turma} (ID: {self.id_turma}, Curso ID: {self.id_curso}, Professor ID: {self.id_professor or 'N/A'})"

    def __repr__(self) -> str:
        return f"Turma(id_turma='{self.id_turma}', nome_turma='{self.nome_turma}')"
