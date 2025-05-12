# src/models/turma.py
from .curso import Curso

# Representa uma turma vinculada a um curso específico
class Turma:
    def __init__(self, id: str, curso: Curso, horario: str):
        self.id = id
        self.curso = curso  # Associação: Turma conhece o curso
        self.horario = horario
        self.alunos: list['Aluno'] = []  # Lista de alunos matriculados

    def matricular_aluno(self, aluno: 'Aluno'):
        # Adiciona aluno à turma
        self.alunos.append(aluno)
        print(f"Aluno {aluno.nome} matriculado na turma {self.id}.")
