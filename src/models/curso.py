# src/models/curso.py
# Representa um curso oferecido na plataforma
class Curso:
    def __init__(self, id: str, nome: str):
        self.id = id
        self.nome = nome

    def __str__(self):
        return f"<Curso {self.nome} ({self.id})>"