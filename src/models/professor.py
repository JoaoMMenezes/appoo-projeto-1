# src/models/professor.py
from .usuario import Usuario

class Professor(Usuario):
    """
    Representa um professor, herda de Usuario.
    """
    def __init__(self, id: str, nome: str, email: str, senha: str, disciplinas: list[str]):
        super().__init__(id, nome, email, senha)
        self.disciplinas = disciplinas

    def autenticar(self, senha: str) -> bool:
        return senha == self._senha

    def publicar_aula(self, aula_id: str):
        print(f"Professor {self.nome} publicou a aula {aula_id}.")
