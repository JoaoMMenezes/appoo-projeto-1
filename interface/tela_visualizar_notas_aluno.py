# interface/tela_visualizar_notas_aluno.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from main import AppController

class TelaVisualizarNotasAluno(tk.Toplevel):
    """
    Tela para Alunos visualizarem suas avaliações (notas e feedbacks).
    """
    def __init__(self, master, app_controller: 'AppController', id_aluno_logado: str):
        super().__init__(master)
        self.app_controller = app_controller
        self.id_aluno_logado = id_aluno_logado
        
        self.transient(master)
        self.grab_set()
        self.title("Minhas Avaliações")
        self.geometry("850x500")

        self._configurar_interface()
        self._carregar_avaliacoes_aluno()

    def _configurar_interface(self):
        frame_principal = ttk.Frame(self, padding=10)
        frame_principal.pack(expand=True, fill=tk.BOTH)

        lbl_titulo = ttk.Label(frame_principal, text="Minhas Notas e Feedbacks", font=('Helvetica', 16, 'bold'))
        lbl_titulo.pack(pady=(0,10))

        # Treeview para exibir as avaliações
        colunas = ("atividade", "turma", "nota", "feedback", "data_lancamento")
        self.tree_avaliacoes = ttk.Treeview(frame_principal, columns=colunas, show="headings", height=15, selectmode="browse")
        
        self.tree_avaliacoes.heading("atividade", text="Atividade")
        self.tree_avaliacoes.heading("turma", text="Turma")
        self.tree_avaliacoes.heading("nota", text="Nota")
        self.tree_avaliacoes.heading("feedback", text="Feedback do Professor")
        self.tree_avaliacoes.heading("data_lancamento", text="Data de Lançamento")

        self.tree_avaliacoes.column("atividade", width=200, minwidth=150)
        self.tree_avaliacoes.column("turma", width=150, minwidth=120)
        self.tree_avaliacoes.column("nota", width=80, minwidth=60, anchor="center")
        self.tree_avaliacoes.column("feedback", width=250, minwidth=200)
        self.tree_avaliacoes.column("data_lancamento", width=120, minwidth=100, anchor="center")
        
        scrollbar_y = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL, command=self.tree_avaliacoes.yview)
        self.tree_avaliacoes.configure(yscrollcommand=scrollbar_y.set)
        
        self.tree_avaliacoes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Botão Fechar
        btn_fechar = ttk.Button(self, text="Fechar", command=self.destroy)
        btn_fechar.pack(pady=10, side=tk.BOTTOM)

    def _carregar_avaliacoes_aluno(self):
        for i in self.tree_avaliacoes.get_children():
            self.tree_avaliacoes.delete(i)

        # Este método no AppController precisará buscar as avaliações
        # e também os nomes/títulos das atividades e turmas associadas.
        avaliacoes_formatadas: List[Dict] = self.app_controller.obter_avaliacoes_formatadas_aluno(self.id_aluno_logado)
        
        if not avaliacoes_formatadas:
            self.tree_avaliacoes.insert("", tk.END, values=("Você ainda não possui avaliações lançadas.", "", "", "", ""))
        else:
            for avaliacao_data in avaliacoes_formatadas:
                self.tree_avaliacoes.insert("", tk.END, 
                                        values=(avaliacao_data["titulo_atividade"],
                                                avaliacao_data["nome_turma"],
                                                avaliacao_data["nota"],
                                                avaliacao_data["feedback"],
                                                avaliacao_data["data_lancamento"]))

# Teste isolado
if __name__ == '__main__':
    class MockAppController:
        def obter_avaliacoes_formatadas_aluno(self, id_aluno):
            if id_aluno == "aluno_com_notas":
                return [
                    {"titulo_atividade": "Trabalho 1 - Python", "nome_turma": "PY-MANHA-2025", "nota": "8.5", "feedback": "Bom trabalho!", "data_lancamento": "2025-05-20 10:00:00"},
                    {"titulo_atividade": "Prova Parcial 1", "nome_turma": "PY-MANHA-2025", "nota": "7.0", "feedback": "Pode melhorar na questão 3.", "data_lancamento": "2025-05-25 14:30:00"},
                    {"titulo_atividade": "Projeto HTML", "nome_turma": "WEB-TARDE-2025", "nota": "Aprovado", "feedback": "Layout criativo.", "data_lancamento": "2025-05-28 11:00:00"},
                ]
            return []

    root = tk.Tk()
    root.withdraw()
    mock_controller = MockAppController()
    tela_notas = TelaVisualizarNotasAluno(root, mock_controller, "aluno_com_notas")
    root.mainloop()
