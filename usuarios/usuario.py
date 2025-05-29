 # usuarios/usuario.py
from abc import ABC, abstractmethod
import hashlib # Para hashing de senhas

class Usuario(ABC):
    """
    Classe base abstrata para todos os tipos de usuários do sistema.

    Atributos:
        id_usuario (str): Identificador único do usuário.
        nome (str): Nome completo do usuário.
        email (str): Endereço de e-mail do usuário.
        _senha_hash (str): Hash da senha do usuário (não armazenar senha em texto plano).
    """

    def __init__(self, id_usuario: str, nome: str, email: str, senha: str):
        """
        Construtor da classe Usuario.

        Args:
            id_usuario (str): ID do usuário.
            nome (str): Nome do usuário.
            email (str): Email do usuário.
            senha (str): Senha em texto plano (será hasheada).
        """
        if not all([id_usuario, nome, email, senha]):
            raise ValueError("ID, nome, email e senha são obrigatórios.")
        
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self._senha_hash = self._hash_senha(senha) # Armazena o hash da senha

    def _hash_senha(self, senha: str) -> str:
        """
        Gera um hash SHA256 para a senha fornecida.

        Args:
            senha (str): A senha em texto plano.

        Returns:
            str: O hash hexadecimal da senha.
        """
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def verificar_senha(self, senha_fornecida: str) -> bool:
        """
        Verifica se a senha fornecida corresponde à senha armazenada.

        Args:
            senha_fornecida (str): A senha em texto plano para verificação.

        Returns:
            bool: True se as senhas corresponderem, False caso contrário.
        """
        return self._senha_hash == self._hash_senha(senha_fornecida)

    @abstractmethod
    def obter_tipo_usuario(self) -> str:
        """
        Método abstrato para retornar o tipo de usuário (Aluno, Professor, Coordenador).
        Deve ser implementado pelas subclasses.

        Returns:
            str: O tipo de usuário.
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Método abstrato para converter o objeto Usuario em um dicionário,
        útil para serialização JSON.

        Returns:
            dict: Uma representação do usuário em dicionário.
        """
        return {
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "email": self.email,
            "_senha_hash": self._senha_hash, # Incluir o hash para persistência
            "tipo": self.obter_tipo_usuario()
        }

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """
        Método de classe abstrato para criar uma instância de Usuario (ou subclasse)
        a partir de um dicionário.

        Args:
            data (dict): Dicionário contendo os dados do usuário.

        Returns:
            Usuario: Uma instância da subclasse de Usuario.
        """
        # A senha não estará no dict como 'senha', mas como '_senha_hash'
        # Este método precisará ser implementado cuidadosamente nas subclasses
        # para lidar com a recriação do objeto sem a senha original em texto plano.
        # Para o propósito de carregar, podemos precisar de um construtor alternativo
        # ou ajustar o __init__ para aceitar _senha_hash diretamente.
        # Por ora, vamos assumir que o from_dict das subclasses lidará com isso.
        pass

    def __str__(self) -> str:
        return f"{self.obter_tipo_usuario()}: {self.nome} (ID: {self.id_usuario}, Email: {self.email})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id_usuario='{self.id_usuario}', nome='{self.nome}', email='{self.email}')"

