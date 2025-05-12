# src/models/aula_pratica.py
from .conteudo import Conteudo

# Conteúdo de tipo Prática
class AulaPratica(Conteudo):
    def __init__(self, id: str, titulo: str, guia: str):
        self.id = id
        self.titulo = titulo
        self.guia = guia

    def exibir(self):
        # Mostra as instruções práticas
        print(f"Exibindo prática: {self.titulo}")

    def avaliar(self):
        # Corrige e atribui nota à prática
        print(f"Corrigindo prática: {self.titulo}")