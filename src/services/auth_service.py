# src/services/auth_service.py
from typing import Optional
from src.services.database_service import DatabaseService
from src.models.usuario import Usuario

class AuthService:
    """
    Serviço de autenticação que consulta o DatabaseService.
    """
    def __init__(self, db: DatabaseService):
        self.db = db

    def register(self, usuario: Usuario) -> bool:
        if self.db.get_user(usuario.email):
            print("Email já cadastrado.")
            return False
        self.db.save_user(usuario)
        return True

    def login(self, email: str, senha: str) -> Optional[Usuario]:
        u = self.db.get_user(email)
        if not u:
            print("Usuário não encontrado.")
            return None
        if u.get("senha") != senha:
            print("Senha incorreta.")
            return None
        print(f"Login bem-sucedido para {u.get('nome')}.")
        tipo = u.get("tipo")
        if tipo == "Aluno":
            from src.models.aluno import Aluno
            return Aluno(u["id"], u["nome"], u["email"], u["senha"], turma_id="")
        if tipo == "Professor":
            from src.models.professor import Professor
            return Professor(u["id"], u["nome"], u["email"], u["senha"], disciplinas=[])
        if tipo == "Coordenador":
            from src.models.coordenador import Coordenador
            return Coordenador(u["id"], u["nome"], u["email"], u["senha"])
        return None