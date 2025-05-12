# src/models/aluno.py
from .usuario import Usuario

class Aluno(Usuario):
    """
    Representa um aluno, herda de Usuario.
    """
    def __init__(self, id: str, nome: str, email: str, senha: str, turma_id: str):
        super().__init__(id, nome, email, senha)
        self.turma_id = turma_id

    def autenticar(self, senha: str) -> bool:
        # Autenticação simples comparando strings (exemplo)
        return senha == self._senha

    def solicitar_avaliacao(self):
        print(f"Aluno {self.nome} solicitou avaliação para a turma {self.turma_id}.")
