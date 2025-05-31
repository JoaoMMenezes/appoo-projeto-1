# entidades/curso.py

class Curso:
    """
    Representa um curso oferecido pela instituição.

    Atributos:
        id_curso (str): Identificador único do curso.
        nome_curso (str): Nome do curso.
        descricao (str): Descrição detalhada do curso.
        carga_horaria (int): Carga horária total do curso em horas.
        lista_id_turmas (list[str]): Lista de IDs das turmas associadas a este curso.
    """

    def __init__(self, id_curso: str, nome_curso: str, descricao: str, carga_horaria: int):
        """
        Construtor da classe Curso.

        Args:
            id_curso (str): ID do curso.
            nome_curso (str): Nome do curso.
            descricao (str): Descrição do curso.
            carga_horaria (int): Carga horária em horas.
        """
        if not all([id_curso, nome_curso, descricao]):
            raise ValueError("ID, nome e descrição do curso são obrigatórios.")
        if not isinstance(carga_horaria, int) or carga_horaria <= 0:
            raise ValueError("Carga horária deve ser um inteiro positivo.")

        self.id_curso = id_curso
        self.nome_curso = nome_curso
        self.descricao = descricao
        self.carga_horaria = carga_horaria
        self.lista_id_turmas = [] # Inicializa como lista vazia

    def adicionar_turma(self, id_turma: str):
        """Adiciona o ID de uma turma à lista de turmas do curso."""
        if id_turma not in self.lista_id_turmas:
            self.lista_id_turmas.append(id_turma)

    def remover_turma(self, id_turma: str):
        """Remove o ID de uma turma da lista de turmas do curso."""
        if id_turma in self.lista_id_turmas:
            self.lista_id_turmas.remove(id_turma)

    def to_dict(self) -> dict:
        """
        Converte o objeto Curso em um dicionário para serialização.

        Returns:
            dict: Dicionário representando o curso.
        """
        return {
            "id_curso": self.id_curso,
            "nome_curso": self.nome_curso,
            "descricao": self.descricao,
            "carga_horaria": self.carga_horaria,
            "lista_id_turmas": self.lista_id_turmas
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria um objeto Curso a partir de um dicionário.

        Args:
            data (dict): Dicionário com os dados do curso.

        Returns:
            Curso: Uma instância da classe Curso.
        """
        curso = cls(
            id_curso=data["id_curso"],
            nome_curso=data["nome_curso"],
            descricao=data["descricao"],
            carga_horaria=data["carga_horaria"]
        )
        curso.lista_id_turmas = data.get("lista_id_turmas", [])
        return curso

    def __str__(self) -> str:
        return f"Curso: {self.nome_curso} (ID: {self.id_curso}, Carga Horária: {self.carga_horaria}h)"

    def __repr__(self) -> str:
        return f"Curso(id_curso='{self.id_curso}', nome_curso='{self.nome_curso}')"
