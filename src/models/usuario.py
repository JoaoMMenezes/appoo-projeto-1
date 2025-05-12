# src/models/usuario.py
from abc import ABC, abstractmethod

class Usuario(ABC):
    """
    Classe abstrata que define a interface de usuários.
    """
    def __init__(self, id: str, nome: str, email: str, senha: str):
        self.id = id
        self.nome = nome
        self.email = email
        self._senha = senha  # senha armazenada (em produção, hasheada)

    @abstractmethod
    def autenticar(self, senha: str) -> bool:
        """
        Verifica se a senha fornecida bate com a senha do usuário.
        """
        pass

    def __str__(self):
        return f"<Usuario {self.nome} ({self.id})>"