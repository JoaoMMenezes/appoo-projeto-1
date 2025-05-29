# interface/tela_listar_cursos_aluno.py
import tkinter as tk
from tkinter import ttk, messagebox

class TelaListarCursosAluno(tk.Toplevel):
    """
    Tela para Alunos listarem os cursos disponíveis.
    """
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller
        self.transient(master)
        self.grab_set()
        self.title("Cursos Disponíveis")
        self.geometry("700x500")

        self._configurar_interface()
        self._carregar_cursos()

    def _configurar_interface(self):
        frame_principal = ttk.Frame(self, padding=(10, 10))
        frame_principal.pack(fill="both", expand=True)

        lbl_titulo = ttk.Label(frame_principal, text="Cursos Oferecidos", font=('Helvetica', 16, 'bold'))
        lbl_titulo.pack(pady=(0,10))

        colunas = ("nome_curso", "descricao", "carga_horaria")
        self.tree_cursos_disp = ttk.Treeview(frame_principal, columns=colunas, show="headings", height=15)
        
        self.tree_cursos_disp.heading("nome_curso", text="Nome do Curso")
        self.tree_cursos_disp.heading("descricao", text="Descrição")
        self.tree_cursos_disp.heading("carga_horaria", text="C.H.")

        self.tree_cursos_disp.column("nome_curso", width=200, minwidth=150)
        self.tree_cursos_disp.column("descricao", width=350, minwidth=250)
        self.tree_cursos_disp.column("carga_horaria", width=80, minwidth=60, anchor="center")

        # Scrollbar
        scrollbar_tree = ttk.Scrollbar(frame_principal, orient="vertical", command=self.tree_cursos_disp.yview)
        self.tree_cursos_disp.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_cursos_disp.pack(side="left", fill="both", expand=True)
        scrollbar_tree.pack(side="right", fill="y")
        
        # Adicionar informações sobre como se inscrever ou um botão (placeholder por enquanto)
        # lbl_info_inscricao = ttk.Label(frame_principal, text="Para se inscrever em um curso, vá para 'Inscrever-se em Turma'.")
        # lbl_info_inscricao.pack(pady=10)

        btn_fechar = ttk.Button(self, text="Fechar", command=self.destroy) # Botão no Toplevel, não no frame_principal
        btn_fechar.pack(pady=10)


    def _carregar_cursos(self):
        """Carrega os cursos do controller e os exibe na Treeview."""
        for i in self.tree_cursos_disp.get_children():
            self.tree_cursos_disp.delete(i)
            
        cursos = self.app_controller.obter_cursos()
        if not cursos:
            self.tree_cursos_disp.insert("", tk.END, values=("Nenhum curso cadastrado ainda.", "", ""))
        else:
            for curso in cursos:
                # Usar o nome do curso como iid aqui é aceitável para exibição simples,
                # mas se IDs fossem clicáveis para mais ações, usar curso.id_curso seria melhor.
                self.tree_cursos_disp.insert("", tk.END, values=(curso.nome_curso, curso.descricao, curso.carga_horaria))


# Para testar esta tela isoladamente (opcional)
if __name__ == '__main__':
    class MockAppController:
        def __init__(self):
            self.cursos_mock = []
            # from entidades.curso import Curso # Se o arquivo estiver em um local diferente
            # Simular alguns cursos
            CursoMock = type("CursoMock", (), {"id_curso": "", "nome_curso": "", "descricao": "", "carga_horaria": 0})
            
            c1 = CursoMock()
            c1.id_curso = "c001"
            c1.nome_curso = "Python para Iniciantes"
            c1.descricao = "Aprenda os fundamentos da linguagem Python."
            c1.carga_horaria = 40
            self.cursos_mock.append(c1)

            c2 = CursoMock()
            c2.id_curso = "c002"
            c2.nome_curso = "Desenvolvimento Web com Flask"
            c2.descricao = "Crie aplicações web dinâmicas com Flask."
            c2.carga_horaria = 60
            self.cursos_mock.append(c2)
            
        def obter_cursos(self):
            return self.cursos_mock

    root = tk.Tk()
    root.withdraw() 
    app_controller_mock = MockAppController()
    tela_listar = TelaListarCursosAluno(root, app_controller_mock)
    root.mainloop()
#         return cls(**data)
#         return cls(