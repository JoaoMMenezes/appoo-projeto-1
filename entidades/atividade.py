# entidades/atividade.py

# entidades/atividade.py (revisão, já deve existir)
class Atividade:
    def __init__(self, id_atividade: str, id_turma_ou_curso: str, titulo: str, descricao: str, data_prazo: str, tipo: str):
        if not all([id_atividade, id_turma_ou_curso, titulo, tipo]):
            raise ValueError("ID da atividade, ID da turma/curso, título e tipo são obrigatórios.")
        self.id_atividade = id_atividade
        self.id_turma_ou_curso = id_turma_ou_curso # Usaremos como id_turma
        self.titulo = titulo
        self.descricao = descricao
        self.data_prazo = data_prazo 
        self.tipo = tipo # Ex: "Prova", "Trabalho", "Exercício"

    def to_dict(self) -> dict:
        return {
            "id_atividade": self.id_atividade,
            "id_turma_ou_curso": self.id_turma_ou_curso,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "data_prazo": self.data_prazo,
            "tipo": self.tipo
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_atividade=data["id_atividade"],
            id_turma_ou_curso=data["id_turma_ou_curso"],
            titulo=data["titulo"],
            descricao=data["descricao"],
            data_prazo=data["data_prazo"],
            tipo=data["tipo"]
        )
    # ... __str__ e __repr__ ...

    def __str__(self) -> str:
        return f"Atividade: {self.titulo} (ID: {self.id_atividade}, Tipo: {self.tipo}, Prazo: {self.data_prazo})"

    def __repr__(self) -> str:
        return f"Atividade(id_atividade='{self.id_atividade}', titulo='{self.titulo}')"
