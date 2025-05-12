# src/models/desafio.py
from .conteudo import Conteudo

# Conteúdo de tipo Desafio Avaliativo
class Desafio(Conteudo):
    def __init__(self, id: str, enunciado: str):
        self.id = id
        self.enunciado = enunciado

    def exibir(self):
        print(f"Desafio: {self.enunciado}")

    def avaliar(self):
        print("Corrigindo desafio e atribuindo nota.")
