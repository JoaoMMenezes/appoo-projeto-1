# usuarios/aluno.py
from usuarios.usuario import Usuario

class Aluno(Usuario):
    """
    Representa um aluno no sistema. Herda da classe Usuario.

    Atributos adicionais:
        matricula (str): Número de matrícula do aluno.
        turmas_inscritas (list[str]): Lista de IDs das TURMAS em que o aluno está inscrito.
    """

    def __init__(self, id_usuario: str, nome: str, email: str, senha: str, matricula: str):
        """
        Construtor da classe Aluno.

        Args:
            id_usuario (str): ID do usuário.
            nome (str): Nome do aluno.
            email (str): Email do aluno.
            senha (str): Senha do aluno.
            matricula (str): Número de matrícula do aluno.
        """
        super().__init__(id_usuario, nome, email, senha)
        if not matricula:
            raise ValueError("Matrícula é obrigatória para o aluno.")
        self.matricula = matricula
        self.turmas_inscritas = [] # Alterado de cursos_inscritos para turmas_inscritas

    def obter_tipo_usuario(self) -> str:
        """Retorna o tipo de usuário."""
        return "Aluno"

    def inscrever_em_turma(self, id_turma: str):
        """
        Inscreve o aluno em uma turma.

        Args:
            id_turma (str): ID da turma na qual se inscrever.
        """
        if id_turma not in self.turmas_inscritas: 
            self.turmas_inscritas.append(id_turma)
            print(f"Aluno {self.nome} inscrito na turma {id_turma}.")
        else:
            print(f"Aluno {self.nome} já está inscrito na turma {id_turma}.")

    def cancelar_inscricao_turma(self, id_turma: str):
        """
        Cancela a inscrição do aluno em uma turma.

        Args:
            id_turma (str): ID da turma da qual cancelar a inscrição.
        """
        if id_turma in self.turmas_inscritas:
            self.turmas_inscritas.remove(id_turma)
            print(f"Aluno {self.nome} teve a inscrição cancelada na turma {id_turma}.")
        else:
            print(f"Aluno {self.nome} não está inscrito na turma {id_turma}.")

    def to_dict(self) -> dict:
        """
        Converte o objeto Aluno em um dicionário.
        Sobrescreve o método da classe base para incluir atributos específicos do Aluno.

        Returns:
            dict: Dicionário com os dados do aluno.
        """
        data = super().to_dict()
        data.update({
            "matricula": self.matricula,
            "turmas_inscritas": self.turmas_inscritas # Alterado
        })
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria um objeto Aluno a partir de um dicionário.
        """
        aluno = cls(
            id_usuario=data["id_usuario"],
            nome=data["nome"],
            email=data["email"],
            senha="senha_placeholder_from_dict", 
            matricula=data["matricula"]
        )
        aluno._senha_hash = data["_senha_hash"] 
        aluno.turmas_inscritas = data.get("turmas_inscritas", []) # Alterado e usando .get
        return aluno

    def __str__(self) -> str:
        return f"{super().__str__()} - Matrícula: {self.matricula}"
# usuarios/aluno.py