# interface/tela_gerenciar_turmas.py
import tkinter as tk
from tkinter import ttk, messagebox
import uuid # Para gerar IDs de turma
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import AppController # Para type hinting
    from entidades.curso import Curso
    from usuarios.professor import Professor

class TelaGerenciarTurmas(tk.Toplevel):
    """
    Tela para professores/coordenadores gerenciarem turmas.
    """
    def __init__(self, master, app_controller: 'AppController'):
        super().__init__(master)
        self.app_controller = app_controller
        self.transient(master)
        self.grab_set()
        self.title("Gerenciar Turmas")
        self.geometry("950x650") # Aumentado para acomodar mais campos e a lista

        # Variáveis de controle
        self.id_turma_var = tk.StringVar()
        self.nome_turma_var = tk.StringVar()
        self.id_curso_selecionado_var = tk.StringVar()
        self.id_professor_selecionado_var = tk.StringVar()
        self.max_alunos_var = tk.StringVar()

        # Dicionários para mapear nomes de volta para IDs (para ComboBoxes)
        self.cursos_map = {} # nome_curso -> id_curso
        self.professores_map = {} # nome_professor -> id_professor

        self._configurar_interface()
        self._carregar_dados_para_comboboxes()
        self._carregar_turmas_existentes()

    def _configurar_interface(self):
        # --- Frame para formulário ---
        frame_formulario = ttk.LabelFrame(self, text="Detalhes da Turma", padding=(10, 10))
        frame_formulario.pack(padx=10, pady=10, fill="x", expand=False)

        # ID Turma
        ttk.Label(frame_formulario, text="ID Turma:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_id_turma = ttk.Entry(frame_formulario, textvariable=self.id_turma_var, state="readonly", width=40)
        self.ent_id_turma.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Nome Turma
        ttk.Label(frame_formulario, text="Nome da Turma:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_nome_turma = ttk.Entry(frame_formulario, textvariable=self.nome_turma_var, width=40)
        self.ent_nome_turma.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Curso Associado (ComboBox)
        ttk.Label(frame_formulario, text="Curso:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.cmb_curso = ttk.Combobox(frame_formulario, textvariable=self.id_curso_selecionado_var, state="readonly", width=38)
        self.cmb_curso.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Professor Responsável (ComboBox)
        ttk.Label(frame_formulario, text="Professor:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.cmb_professor = ttk.Combobox(frame_formulario, textvariable=self.id_professor_selecionado_var, state="readonly", width=38)
        self.cmb_professor.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        # Permitir "Nenhum" professor
        self.cmb_professor['values'] = ["Nenhum"] 
        self.id_professor_selecionado_var.set("Nenhum")


        # Máximo de Alunos
        ttk.Label(frame_formulario, text="Máx. Alunos:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.ent_max_alunos = ttk.Entry(frame_formulario, textvariable=self.max_alunos_var, width=10)
        self.ent_max_alunos.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        frame_formulario.columnconfigure(1, weight=1)

        # --- Frame para botões de ação ---
        frame_botoes_acao = ttk.Frame(self, padding=(10, 5))
        frame_botoes_acao.pack(fill="x", expand=False)

        self.btn_novo = ttk.Button(frame_botoes_acao, text="Nova/Limpar", command=self._limpar_formulario)
        self.btn_novo.pack(side="left", padx=5)

        self.btn_salvar = ttk.Button(frame_botoes_acao, text="Salvar Turma", command=self._salvar_turma)
        self.btn_salvar.pack(side="left", padx=5)
        
        self.btn_excluir = ttk.Button(frame_botoes_acao, text="Excluir Selecionada", command=self._excluir_turma)
        self.btn_excluir.pack(side="left", padx=5)

        # --- Frame para lista de turmas ---
        frame_lista = ttk.LabelFrame(self, text="Turmas Cadastradas", padding=(10, 10))
        frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        colunas = ("id_turma", "nome_turma", "curso", "professor", "max_alunos", "vagas_preenchidas")
        self.tree_turmas = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=10)
        
        self.tree_turmas.heading("id_turma", text="ID Turma")
        self.tree_turmas.heading("nome_turma", text="Nome da Turma")
        self.tree_turmas.heading("curso", text="Curso")
        self.tree_turmas.heading("professor", text="Professor")
        self.tree_turmas.heading("max_alunos", text="Máx. Alunos")
        self.tree_turmas.heading("vagas_preenchidas", text="Inscritos")

        self.tree_turmas.column("id_turma", width=180, minwidth=150, stretch=tk.NO)
        self.tree_turmas.column("nome_turma", width=150, minwidth=120)
        self.tree_turmas.column("curso", width=180, minwidth=150)
        self.tree_turmas.column("professor", width=150, minwidth=120)
        self.tree_turmas.column("max_alunos", width=80, minwidth=70, anchor="center")
        self.tree_turmas.column("vagas_preenchidas", width=80, minwidth=70, anchor="center")

        scrollbar_tree = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_turmas.yview)
        self.tree_turmas.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_turmas.pack(side="left", fill="both", expand=True)
        scrollbar_tree.pack(side="right", fill="y")

        self.tree_turmas.bind("<<TreeviewSelect>>", self._ao_selecionar_turma)

        btn_fechar = ttk.Button(self, text="Fechar", command=self.destroy)
        btn_fechar.pack(pady=10)
        
        self._limpar_formulario()

    def _carregar_dados_para_comboboxes(self):
        """Carrega cursos e professores para os ComboBoxes."""
        # Cursos
        cursos_obj: list['Curso'] = self.app_controller.obter_cursos()
        nomes_cursos = [c.nome_curso for c in cursos_obj]
        self.cursos_map = {c.nome_curso: c.id_curso for c in cursos_obj}
        self.cmb_curso['values'] = nomes_cursos
        if nomes_cursos:
            self.id_curso_selecionado_var.set(nomes_cursos[0]) # Seleciona o primeiro por padrão

        # Professores
        professores_obj: list['Professor'] = self.app_controller.obter_professores() # Precisa existir no AppController
        nomes_professores = ["Nenhum"] + [p.nome for p in professores_obj]
        self.professores_map = {p.nome: p.id_usuario for p in professores_obj}
        self.professores_map["Nenhum"] = None # Mapeia "Nenhum" para None
        self.cmb_professor['values'] = nomes_professores
        self.id_professor_selecionado_var.set("Nenhum") # Padrão

    def _limpar_formulario(self):
        self.id_turma_var.set(str(uuid.uuid4()))
        self.nome_turma_var.set("")
        if self.cmb_curso['values']: # Se houver cursos
            self.id_curso_selecionado_var.set(self.cmb_curso['values'][0])
        else:
            self.id_curso_selecionado_var.set("")
        self.id_professor_selecionado_var.set("Nenhum")
        self.max_alunos_var.set("")
        self.ent_nome_turma.focus()
        if self.tree_turmas.selection():
            self.tree_turmas.selection_remove(self.tree_turmas.selection())

    def _carregar_turmas_existentes(self):
        for i in self.tree_turmas.get_children():
            self.tree_turmas.delete(i)
            
        turmas = self.app_controller.obter_turmas()
        for turma in turmas:
            curso_obj = self.app_controller.obter_curso_por_id(turma.id_curso)
            nome_curso = curso_obj.nome_curso if curso_obj else "N/A"
            
            professor_obj = self.app_controller.obter_professor_por_id(turma.id_professor) if turma.id_professor else None
            nome_professor = professor_obj.nome if professor_obj else "Nenhum"
            
            vagas_preenchidas = len(turma.lista_id_alunos)
            
            self.tree_turmas.insert("", tk.END, values=(
                turma.id_turma, turma.nome_turma, nome_curso, nome_professor, turma.max_alunos, vagas_preenchidas
            ), iid=turma.id_turma)

    def _ao_selecionar_turma(self, event=None):
        selecionado = self.tree_turmas.selection()
        if not selecionado:
            return

        id_turma_selecionada = selecionado[0]
        turma = self.app_controller.obter_turma_por_id(id_turma_selecionada)

        if turma:
            self.id_turma_var.set(turma.id_turma)
            self.nome_turma_var.set(turma.nome_turma)
            self.max_alunos_var.set(str(turma.max_alunos))

            # Selecionar curso no ComboBox
            curso_obj = self.app_controller.obter_curso_por_id(turma.id_curso)
            if curso_obj:
                self.id_curso_selecionado_var.set(curso_obj.nome_curso)
            else:
                self.id_curso_selecionado_var.set("") # Ou um valor padrão se o curso não existir mais

            # Selecionar professor no ComboBox
            if turma.id_professor:
                professor_obj = self.app_controller.obter_professor_por_id(turma.id_professor)
                if professor_obj:
                    self.id_professor_selecionado_var.set(professor_obj.nome)
                else: # Professor pode ter sido removido
                    self.id_professor_selecionado_var.set("Nenhum")
            else:
                self.id_professor_selecionado_var.set("Nenhum")
        else:
            messagebox.showerror("Erro", f"Turma com ID {id_turma_selecionada} não encontrada.")
            self._limpar_formulario()

    def _salvar_turma(self):
        id_turma = self.id_turma_var.get()
        nome_turma = self.nome_turma_var.get().strip()
        nome_curso_selecionado = self.id_curso_selecionado_var.get()
        nome_professor_selecionado = self.id_professor_selecionado_var.get()
        max_alunos_str = self.max_alunos_var.get().strip()

        if not nome_turma or not nome_curso_selecionado or not max_alunos_str:
            messagebox.showerror("Erro de Validação", "Nome da turma, curso e máx. alunos são obrigatórios.")
            return

        id_curso = self.cursos_map.get(nome_curso_selecionado)
        if not id_curso:
            messagebox.showerror("Erro de Validação", "Curso selecionado inválido.")
            return
            
        id_professor = self.professores_map.get(nome_professor_selecionado, None) # Permite None

        try:
            max_alunos = int(max_alunos_str)
            if max_alunos <= 0:
                raise ValueError("Máximo de alunos deve ser positivo.")
        except ValueError:
            messagebox.showerror("Erro de Validação", "Máximo de Alunos deve ser um número inteiro positivo.")
            return

        turma_existente = self.app_controller.obter_turma_por_id(id_turma)

        if turma_existente: # Atualização
            sucesso, mensagem = self.app_controller.atualizar_turma(id_turma, id_curso, nome_turma, max_alunos, id_professor)
        else: # Nova turma
            sucesso, mensagem = self.app_controller.criar_turma(id_curso, nome_turma, max_alunos, id_professor, id_turma_manual=id_turma)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self._carregar_turmas_existentes()
            self._limpar_formulario()
        else:
            messagebox.showerror("Erro", mensagem)

    def _excluir_turma(self):
        selecionado = self.tree_turmas.selection()
        if not selecionado:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma turma para excluir.")
            return

        id_turma_selecionada = selecionado[0]
        
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a turma ID: {id_turma_selecionada}? Isso NÃO desinscreverá os alunos automaticamente (funcionalidade futura)."):
            sucesso, mensagem = self.app_controller.excluir_turma(id_turma_selecionada)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self._carregar_turmas_existentes()
                self._limpar_formulario()
            else:
                messagebox.showerror("Erro", mensagem)

# Para testar esta tela isoladamente (opcional)
if __name__ == '__main__':
    # Mock para Curso e Professor para o teste da tela
    CursoMock = type("CursoMock", (), {"id_curso": "", "nome_curso": "", "descricao": "", "carga_horaria": 0})
    ProfessorMock = type("ProfessorMock", (), {"id_usuario": "", "nome": "", "email": "", "_senha_hash": "", "departamento": "", "turmas_lecionadas": []})
    TurmaMock = type("TurmaMock", (), {"id_turma": "", "id_curso": "", "id_professor": None, "nome_turma": "", "max_alunos": 0, "lista_id_alunos": []})

    class MockAppController:
        def __init__(self):
            self.cursos = []
            self.professores = []
            self.turmas = []

            c1 = CursoMock(); c1.id_curso="c001"; c1.nome_curso="Python Básico"; self.cursos.append(c1)
            c2 = CursoMock(); c2.id_curso="c002"; c2.nome_curso="Web com Django"; self.cursos.append(c2)

            p1 = ProfessorMock(); p1.id_usuario="p001"; p1.nome="Prof. Ada"; self.professores.append(p1)
            p2 = ProfessorMock(); p2.id_usuario="p002"; p2.nome="Prof. Alan"; self.professores.append(p2)
            
            t1 = TurmaMock(); t1.id_turma="t001"; t1.nome_turma="PY01-2025"; t1.id_curso="c001"; t1.id_professor="p001"; t1.max_alunos=20; self.turmas.append(t1)


        def obter_cursos(self): return self.cursos
        def obter_professores(self): return self.professores
        def obter_turmas(self): return self.turmas
        def obter_curso_por_id(self, id_c): return next((c for c in self.cursos if c.id_curso == id_c), None)
        def obter_professor_por_id(self, id_p): return next((p for p in self.professores if p.id_usuario == id_p), None)
        def obter_turma_por_id(self, id_t): return next((t for t in self.turmas if t.id_turma == id_t), None)

        def criar_turma(self, id_curso, nome_turma, max_alunos, id_professor=None, id_turma_manual=None):
            nova_id = id_turma_manual if id_turma_manual else str(uuid.uuid4())
            if any(t.id_turma == nova_id for t in self.turmas): return False, "ID já existe"
            nt = TurmaMock(); nt.id_turma=nova_id; nt.id_curso=id_curso; nt.nome_turma=nome_turma; nt.max_alunos=max_alunos; nt.id_professor=id_professor; nt.lista_id_alunos=[]
            self.turmas.append(nt)
            return True, f"Turma '{nome_turma}' criada."

        def atualizar_turma(self, id_turma, id_curso, nome_turma, max_alunos, id_professor=None):
            turma = self.obter_turma_por_id(id_turma)
            if turma:
                turma.id_curso=id_curso; turma.nome_turma=nome_turma; turma.max_alunos=max_alunos; turma.id_professor=id_professor
                return True, f"Turma '{nome_turma}' atualizada."
            return False, "Turma não encontrada."

        def excluir_turma(self, id_turma):
            turma = self.obter_turma_por_id(id_turma)
            if turma:
                self.turmas.remove(turma)
                return True, f"Turma ID {id_turma} excluída."
            return False, "Turma não encontrada."

    root = tk.Tk()
    root.withdraw()
    app_controller_mock = MockAppController()
    tela_gerenciar = TelaGerenciarTurmas(root, app_controller_mock)
    root.mainloop()
