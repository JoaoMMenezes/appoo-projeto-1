# src/models/avaliacao.py
# Registra nota de avaliação para um aluno em um conteúdo
class Avaliacao:
    def __init__(self, id: str, aluno_id: str, conteudo_id: str, nota: float):
        self.id = id
        self.aluno_id = aluno_id
        self.conteudo_id = conteudo_id
        self.nota = nota

    def __str__(self):
        return f"<Avaliacao {self.id}: aluno={self.aluno_id}, nota={self.nota}>"
