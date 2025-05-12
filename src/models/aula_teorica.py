# src/models/aula_teorica.py
from .conteudo import Conteudo

# Conteúdo de tipo Teoria
class AulaTeorica(Conteudo):
    def __init__(self, id: str, titulo: str, material: str):
        # Identificador, título e link ou texto do material teórico
        self.id = id
        self.titulo = titulo
        self.material = material

    def exibir(self):
        # Implementação de exibição de teoria
        print(f"Exibindo teoria: {self.titulo}")

    def avaliar(self):
        # Não aplicável para aulas teóricas
        print("Avaliação não aplicável para aula teórica.")

