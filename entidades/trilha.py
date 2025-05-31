# entidades/trilha.py
import uuid

class TrilhaAprendizagem:
    """
    Representa uma Trilha de Aprendizagem, uma sequência de cursos e/ou atividades.
    """
    def __init__(self, id_trilha: str, nome_trilha: str, descricao: str, 
                 sequencia_itens: list = None, publico_alvo: str = ""):
        """
        Construtor da TrilhaAprendizagem.

        Args:
            id_trilha (str): Identificador único da trilha.
            nome_trilha (str): Nome da trilha.
            descricao (str): Descrição da trilha.
            sequencia_itens (list, optional): Lista de dicionários representando os itens da trilha.
                                             Cada dict: {"tipo": "curso"|"atividade", "id_item": "uuid_do_item"}
                                             Defaults to None, que se torna [].
            publico_alvo (str, optional): Descrição do público alvo da trilha. Defaults to "".
        """
        if not all([id_trilha, nome_trilha, descricao]):
            raise ValueError("ID, Nome e Descrição da trilha são obrigatórios.")

        self.id_trilha = id_trilha
        self.nome_trilha = nome_trilha
        self.descricao = descricao
        self.sequencia_itens = sequencia_itens if sequencia_itens is not None else []
        self.publico_alvo = publico_alvo
        # id_coordenador_criador pode ser adicionado futuramente

    def adicionar_item(self, tipo_item: str, id_item: str, nome_item_para_referencia: str = ""):
        """
        Adiciona um item (curso ou atividade) à sequência da trilha.

        Args:
            tipo_item (str): "curso" ou "atividade".
            id_item (str): ID do curso ou da atividade.
            nome_item_para_referencia (str): Nome/título do item, para facilitar a visualização (opcional).
        """
        if tipo_item not in ["curso", "atividade"]:
            raise ValueError("Tipo de item inválido. Deve ser 'curso' ou 'atividade'.")
        self.sequencia_itens.append({
            "tipo": tipo_item, 
            "id_item": id_item,
            "nome_referencia": nome_item_para_referencia # Adicionado para facilitar display
        })

    def remover_item(self, indice: int):
        """Remove um item da trilha pelo seu índice na sequência."""
        if 0 <= indice < len(self.sequencia_itens):
            del self.sequencia_itens[indice]
        else:
            raise IndexError("Índice fora do intervalo da sequência de itens.")

    def to_dict(self) -> dict:
        """Converte o objeto TrilhaAprendizagem para um dicionário."""
        return {
            "id_trilha": self.id_trilha,
            "nome_trilha": self.nome_trilha,
            "descricao": self.descricao,
            "sequencia_itens": self.sequencia_itens,
            "publico_alvo": self.publico_alvo
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Cria um objeto TrilhaAprendizagem a partir de um dicionário."""
        return cls(
            id_trilha=data.get("id_trilha", str(uuid.uuid4())), # Garante ID se faltar
            nome_trilha=data["nome_trilha"],
            descricao=data["descricao"],
            sequencia_itens=data.get("sequencia_itens", []),
            publico_alvo=data.get("publico_alvo", "")
        )

    def __str__(self) -> str:
        return f"Trilha: {self.nome_trilha} (ID: {self.id_trilha})"

    def __repr__(self) -> str:
        return f"TrilhaAprendizagem(id_trilha='{self.id_trilha}', nome_trilha='{self.nome_trilha}')"
