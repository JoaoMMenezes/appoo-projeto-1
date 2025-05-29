# entidades/avaliacao.py
import uuid
from datetime import datetime

class Avaliacao:
    """
    Representa a avaliação (nota/feedback) de um aluno para uma atividade específica.
    """
    def __init__(self, id_avaliacao: str, id_aluno: str, id_atividade: str, id_turma: str, 
                 nota: str | float, feedback_professor: str = "", 
                 data_lancamento: str = None, id_professor_avaliador: str = None):
        """
        Construtor da Avaliacao.

        Args:
            id_avaliacao (str): Identificador único da avaliação.
            id_aluno (str): ID do aluno avaliado.
            id_atividade (str): ID da atividade avaliada.
            id_turma (str): ID da turma onde a atividade ocorreu.
            nota (str | float): Nota atribuída (pode ser numérica ou textual como "Aprovado").
            feedback_professor (str, optional): Feedback do professor. Defaults to "".
            data_lancamento (str, optional): Data do lançamento da nota (YYYY-MM-DD HH:MM:SS). 
                                             Defaults to None (data atual será usada).
            id_professor_avaliador (str, optional): ID do professor que lançou a nota. Defaults to None.
        """
        if not all([id_avaliacao, id_aluno, id_atividade, id_turma]): # Nota pode ser 0 ou ""
            raise ValueError("ID da avaliação, ID do aluno, ID da atividade e ID da turma são obrigatórios.")

        self.id_avaliacao = id_avaliacao
        self.id_aluno = id_aluno
        self.id_atividade = id_atividade
        self.id_turma = id_turma 
        self.nota = nota 
        self.feedback_professor = feedback_professor
        self.data_lancamento = data_lancamento if data_lancamento else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id_professor_avaliador = id_professor_avaliador

    def to_dict(self) -> dict:
        """Converte o objeto Avaliacao para um dicionário."""
        return {
            "id_avaliacao": self.id_avaliacao,
            "id_aluno": self.id_aluno,
            "id_atividade": self.id_atividade,
            "id_turma": self.id_turma,
            "nota": self.nota,
            "feedback_professor": self.feedback_professor,
            "data_lancamento": self.data_lancamento,
            "id_professor_avaliador": self.id_professor_avaliador
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Cria um objeto Avaliacao a partir de um dicionário."""
        return cls(
            id_avaliacao=data.get("id_avaliacao", str(uuid.uuid4())), # Garante ID
            id_aluno=data["id_aluno"],
            id_atividade=data["id_atividade"],
            id_turma=data["id_turma"],
            nota=data["nota"],
            feedback_professor=data.get("feedback_professor", ""),
            data_lancamento=data.get("data_lancamento"), # Mantém o que veio do JSON ou None
            id_professor_avaliador=data.get("id_professor_avaliador")
        )

    def __str__(self) -> str:
        return f"Avaliação (ID: {self.id_avaliacao}): Aluno {self.id_aluno} - Ativ {self.id_atividade} - Nota: {self.nota}"

    def __repr__(self) -> str:
        return f"Avaliacao(id_avaliacao='{self.id_avaliacao}', nota='{self.nota}')"
