# main.py
from src.services.database_service import DatabaseService
from src.services.auth_service import AuthService
from src.models.aluno import Aluno
from src.models.professor import Professor
from src.models.coordenador import Coordenador


def test_database_and_auth():
    db = DatabaseService()
    db.connect()
    auth = AuthService(db)

    # Registra usuários com senha funcional
    a = Aluno("a1", "Ana", "ana@ex.com", "pass123", turma_id="t1")
    p = Professor("p1", "Paulo", "paulo@ex.com", "prof123", disciplinas=["Prog"])
    c = Coordenador("c1", "Carla", "carla@ex.com", "coord123")
    for u in [a, p, c]:
        auth.register(u)

    # Testa logins
    assert auth.login("ana@ex.com", "pass123"), "Falha no login de Ana"
    assert not auth.login("ana@ex.com", "wrong"), "Senha incorreta aceita"
    assert not auth.login("no@user.com", "any"), "Usuário inexistente aceito"

    db.disconnect()
    print("Testes de database e auth concluídos com sucesso.")


if __name__ == "__main__":
    test_database_and_auth()
    print("Teste de autenticação e banco de dados concluído.")
# Teste de autenticação e banco de dados concluído.