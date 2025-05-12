# src/models/conteudo.py
from abc import ABC, abstractmethod

# Classe abstrata para qualquer tipo de conteúdo didático
class Conteudo(ABC):
    """
    Define a interface comum para conteúdos (teoria, prática, desafios).
    Métodos exibir() e avaliar() devem ser implementados.
    """
    @abstractmethod
    def exibir(self):
        """Exibe o conteúdo ao usuário."""
        pass

    @abstractmethod
    def avaliar(self):
        """Executa a avaliação do conteúdo (quando aplicável)."""
        pass