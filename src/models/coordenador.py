# src/models/coordenador.py
from .usuario import Usuario

class Coordenador(Usuario):
    """
    Representa um coordenador, herda de Usuario.
    """
    def __init__(self, id: str, nome: str, email: str, senha: str):
        super().__init__(id, nome, email, senha)

    def autenticar(self, senha: str) -> bool:
        return senha == self._senha

    def gerar_relatorio(self):
        print(f"Coordenador {self.nome} gerou relatório geral.")

