# usuarios/professor.py
from usuarios.usuario import Usuario

class Professor(Usuario):
    """
    Representa um professor no sistema. Herda da classe Usuario.

    Atributos adicionais:
        departamento (str): Departamento ao qual o professor pertence.
        turmas_lecionadas (list[str]): Lista de IDs das turmas que o professor leciona.
    """

    def __init__(self, id_usuario: str, nome: str, email: str, senha: str, departamento: str):
        """
        Construtor da classe Professor.

        Args:
            id_usuario (str): ID do usuário.
            nome (str): Nome do professor.
            email (str): Email do professor.
            senha (str): Senha do professor.
            departamento (str): Departamento do professor.
        """
        super().__init__(id_usuario, nome, email, senha)
        if not departamento:
            raise ValueError("Departamento é obrigatório para o professor.")
        self.departamento = departamento
        self.turmas_lecionadas = [] # Lista de IDs de Turmas

    def obter_tipo_usuario(self) -> str:
        """Retorna o tipo de usuário."""
        return "Professor"

    def adicionar_turma(self, id_turma: str):
        """
        Adiciona uma turma à lista de turmas que o professor leciona.

        Args:
            id_turma (str): ID da turma.
        """
        if id_turma not in self.turmas_lecionadas:
            self.turmas_lecionadas.append(id_turma)
            print(f"Turma {id_turma} adicionada ao Professor {self.nome}.")

    def remover_turma(self, id_turma: str):
        """
        Remove uma turma da lista de turmas que o professor leciona.

        Args:
            id_turma (str): ID da turma.
        """
        if id_turma in self.turmas_lecionadas:
            self.turmas_lecionadas.remove(id_turma)
            print(f"Turma {id_turma} removida do Professor {self.nome}.")

    def to_dict(self) -> dict:
        """
        Converte o objeto Professor em um dicionário.
        Sobrescreve o método da classe base.

        Returns:
            dict: Dicionário com os dados do professor.
        """
        data = super().to_dict()
        data.update({
            "departamento": self.departamento,
            "turmas_lecionadas": self.turmas_lecionadas
        })
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria um objeto Professor a partir de um dicionário.

        Args:
            data (dict): Dicionário com os dados do professor.

        Returns:
            Professor: Uma instância da classe Professor.
        """
        professor = cls(
            id_usuario=data["id_usuario"],
            nome=data["nome"],
            email=data["email"],
            senha="senha_placeholder_from_dict",
            departamento=data["departamento"]
        )
        professor._senha_hash = data["_senha_hash"]
        professor.turmas_lecionadas = data.get("turmas_lecionadas", [])
        return professor

    def __str__(self) -> str:
        return f"{super().__str__()} - Departamento: {self.departamento}"
