# src/services/database_service.py
import json
import os
from typing import Any, Dict, Optional

class DatabaseService:
    """
    Serviço de persistência usando arquivo JSON como banco de dados.
    """
    def __init__(self, path: str = "db.json"):
        self.path = path
        self._data: Dict[str, Any] = {}

    def connect(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        else:
            # estrutura inicial
            self._data = {"users": [], "cursos": [], "turmas": []}
            self._save_file()
        print("Banco JSON carregado.")

    def disconnect(self) -> None:
        self._save_file()
        print("Banco JSON salvo e desconectado.")

    def _save_file(self) -> None:
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        for u in self._data.get("users", []):
            if u.get("email") == email:
                return u
        return None

    def save_user(self, user_obj: Any) -> None:
        # assume user_obj tem atributos id, nome, email, _senha e classe
        entry = {
            "id": user_obj.id,
            "nome": user_obj.nome,
            "email": user_obj.email,
            "senha": user_obj._senha,
            "tipo": user_obj.__class__.__name__
        }
        self._data.setdefault("users", []).append(entry)
        self._save_file()
        print(f"Usuário {user_obj.nome} salvo no banco JSON.")

    def save(self, tabela: str, objeto: Any) -> None:
        self._data.setdefault(tabela, []).append(objeto)
        self._save_file()
        print(f"Objeto salvo em '{tabela}' no banco JSON.")