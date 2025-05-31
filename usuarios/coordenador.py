# usuarios/coordenador.py
from usuarios.usuario import Usuario

class Coordenador(Usuario):
    """
    Representa um coordenador no sistema. Herda da classe Usuario.

    Atributos adicionais:
        area_coordenacao (str): Área de coordenação (ex: "Ensino Médio", "Cursos Técnicos").
    """

    def __init__(self, id_usuario: str, nome: str, email: str, senha: str, area_coordenacao: str):
        """
        Construtor da classe Coordenador.

        Args:
            id_usuario (str): ID do usuário.
            nome (str): Nome do coordenador.
            email (str): Email do coordenador.
            senha (str): Senha do coordenador.
            area_coordenacao (str): Área de coordenação.
        """
        super().__init__(id_usuario, nome, email, senha)
        if not area_coordenacao:
            raise ValueError("Área de coordenação é obrigatória para o coordenador.")
        self.area_coordenacao = area_coordenacao

    def obter_tipo_usuario(self) -> str:
        """Retorna o tipo de usuário."""
        return "Coordenador"

    def to_dict(self) -> dict:
        """
        Converte o objeto Coordenador em um dicionário.
        Sobrescreve o método da classe base.

        Returns:
            dict: Dicionário com os dados do coordenador.
        """
        data = super().to_dict()
        data.update({
            "area_coordenacao": self.area_coordenacao
        })
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria um objeto Coordenador a partir de um dicionário.

        Args:
            data (dict): Dicionário com os dados do coordenador.

        Returns:
            Coordenador: Uma instância da classe Coordenador.
        """
        coordenador = cls(
            id_usuario=data["id_usuario"],
            nome=data["nome"],
            email=data["email"],
            senha="senha_placeholder_from_dict",
            area_coordenacao=data["area_coordenacao"]
        )
        coordenador._senha_hash = data["_senha_hash"]
        return coordenador

    def __str__(self) -> str:
        return f"{super().__str__()} - Área: {self.area_coordenacao}"

