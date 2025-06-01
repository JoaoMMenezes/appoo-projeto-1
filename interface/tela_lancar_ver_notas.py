# interface/tela_lancar_ver_notas.py
import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from typing import TYPE_CHECKING, List, Optional, Dict

if TYPE_CHECKING:
    from main import AppController
    from usuarios.aluno import Aluno
    from entidades.turma import Turma
    from entidades.atividade import Atividade
    from entidades.avaliacao import Avaliacao

class TelaLancarVerNotas(tk.Toplevel):
    """
    Tela para Professores lançarem e visualizarem notas de alunos em atividades.
    """
    def __init__(self, master, app_controller: 'AppController', id_professor_logado: str):
        super().__init__(master)
        self.app_controller = app_controller
        self.id_professor_logado = id_professor_logado
        
        self.transient(master)
        self.grab_set()
        self.title("Lançar e Visualizar Notas")
        self.geometry("1000x700") # Ajuste conforme necessário

        # Variáveis de controle de seleção
        self.id_turma_selecionada_var = tk.StringVar()
        self.id_atividade_selecionada_var = tk.StringVar()
        self.turmas_map = {} # nome_exibicao -> id_turma
        self.atividades_map = {} # nome_exibicao -> id_atividade

        # Variáveis do formulário de avaliação
        self.id_avaliacao_var = tk.StringVar() # Para edição
        self.id_aluno_form_var = tk.StringVar() # ID do aluno cuja nota está sendo editada/lançada
        self.nome_aluno_form_var = tk.StringVar() # Nome do aluno para exibição no form
        self.nota_var = tk.StringVar()
        # feedback_var não precisa, usaremos o Text widget diretamente.

        self._configurar_interface()
        self._carregar_turmas_professor()
        
        self.id_turma_selecionada_var.trace_add("write", self._ao_selecionar_turma)
        self.id_atividade_selecionada_var.trace_add("write", self._ao_selecionar_atividade)


    def _configurar_interface(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Frame de Seleção (Turma e Atividade) ---
        frame_selecao = ttk.LabelFrame(main_frame, text="1. Selecione Turma e Atividade", padding=10)
        frame_selecao.pack(fill=tk.X, pady=(0,10))

        ttk.Label(frame_selecao, text="Minhas Turmas:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cmb_turmas = ttk.Combobox(frame_selecao, textvariable=self.id_turma_selecionada_var, state="readonly", width=40)
        self.cmb_turmas.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_selecao, text="Atividades da Turma:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cmb_atividades = ttk.Combobox(frame_selecao, textvariable=self.id_atividade_selecionada_var, state="disabled", width=40)
        self.cmb_atividades.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        frame_selecao.columnconfigure(1, weight=1)

        # --- Frame Principal (Lista de Alunos/Notas e Formulário) ---
        frame_conteudo = ttk.Frame(main_frame)
        frame_conteudo.pack(fill=tk.BOTH, expand=True, pady=(0,10))

        # Sub-Frame Esquerda: Lista de Alunos e Notas
        frame_lista_alunos_notas = ttk.LabelFrame(frame_conteudo, text="2. Alunos da Turma e Notas Lançadas", padding=10)
        frame_lista_alunos_notas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5))

        cols_tree = ("nome_aluno", "nota", "feedback_resumido") # id_aluno e id_avaliacao serão iid/tags
        self.tree_alunos_notas = ttk.Treeview(frame_lista_alunos_notas, columns=cols_tree, show="headings", height=15, selectmode="browse")
        self.tree_alunos_notas.heading("nome_aluno", text="Aluno")
        self.tree_alunos_notas.heading("nota", text="Nota")
        self.tree_alunos_notas.heading("feedback_resumido", text="Feedback (Início)")
        
        self.tree_alunos_notas.column("nome_aluno", width=200)
        self.tree_alunos_notas.column("nota", width=80, anchor="center")
        self.tree_alunos_notas.column("feedback_resumido", width=250)

        scroll_tree = ttk.Scrollbar(frame_lista_alunos_notas, orient=tk.VERTICAL, command=self.tree_alunos_notas.yview)
        self.tree_alunos_notas.config(yscrollcommand=scroll_tree.set)
        self.tree_alunos_notas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_tree.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_alunos_notas.bind("<<TreeviewSelect>>", self._ao_selecionar_aluno_na_treeview)


        # Sub-Frame Direita: Formulário para Lançar/Editar Nota
        frame_formulario = ttk.LabelFrame(frame_conteudo, text="3. Lançar/Editar Avaliação", padding=10)
        frame_formulario.pack(side=tk.RIGHT, fill=tk.Y, padx=(5,0), ipadx=5)
        
        # ID da Avaliação (oculto ou apenas para debug, não editável diretamente aqui)
        # ttk.Label(frame_formulario, text="ID Avaliação:").grid(row=0, column=0, sticky="w", pady=2)
        # self.ent_id_avaliacao = ttk.Entry(frame_formulario, textvariable=self.id_avaliacao_var, state="readonly")
        # self.ent_id_avaliacao.grid(row=0, column=1, sticky="ew", pady=2)
        
        ttk.Label(frame_formulario, text="Aluno:").grid(row=1, column=0, sticky="w", pady=3, padx=5)
        self.lbl_nome_aluno_form = ttk.Label(frame_formulario, textvariable=self.nome_aluno_form_var, font=('Helvetica', 10, 'bold'))
        self.lbl_nome_aluno_form.grid(row=1, column=1, sticky="ew", pady=3, padx=5)

        ttk.Label(frame_formulario, text="Nota:").grid(row=2, column=0, sticky="w", pady=3, padx=5)
        self.ent_nota = ttk.Entry(frame_formulario, textvariable=self.nota_var, width=25, state="disabled")
        self.ent_nota.grid(row=2, column=1, sticky="ew", pady=3, padx=5)

        ttk.Label(frame_formulario, text="Feedback do Professor:").grid(row=3, column=0, columnspan=2, sticky="w", pady=(10,2), padx=5)
        self.txt_feedback = tk.Text(frame_formulario, height=8, width=35, state="disabled", wrap=tk.WORD)
        self.txt_feedback.grid(row=4, column=0, columnspan=2, sticky="ew", pady=2, padx=5)
        scroll_feedback = ttk.Scrollbar(frame_formulario, orient=tk.VERTICAL, command=self.txt_feedback.yview)
        self.txt_feedback.config(yscrollcommand=scroll_feedback.set)
        scroll_feedback.grid(row=4, column=2, sticky="ns")

        frame_botoes_form = ttk.Frame(frame_formulario)
        frame_botoes_form.grid(row=5, column=0, columnspan=2, pady=15)
        self.btn_salvar_avaliacao = ttk.Button(frame_botoes_form, text="Salvar Avaliação", command=self._salvar_avaliacao, state="disabled")
        self.btn_salvar_avaliacao.pack(side=tk.LEFT, padx=5)
        self.btn_limpar_form = ttk.Button(frame_botoes_form, text="Limpar", command=self._limpar_formulario_avaliacao, state="disabled")
        self.btn_limpar_form.pack(side=tk.LEFT, padx=5)
        # Botão para excluir avaliação pode ser adicionado aqui se necessário.
        
        frame_formulario.columnconfigure(1, weight=1)

        # --- Botão Fechar ---
        btn_fechar_janela = ttk.Button(main_frame, text="Fechar Janela", command=self.destroy)
        btn_fechar_janela.pack(pady=10, side=tk.BOTTOM)

    def _carregar_turmas_professor(self):
        self.turmas_map.clear()
        turmas_obj: List['Turma'] = self.app_controller.obter_turmas_por_professor(self.id_professor_logado)
        nomes_turmas_exibicao = []
        if turmas_obj:
            for turma in turmas_obj:
                curso = self.app_controller.obter_curso_por_id(turma.id_curso)
                nome_exib = f"{turma.nome_turma} ({curso.nome_curso if curso else 'N/A'}) - ID: {turma.id_turma[:8]}"
                nomes_turmas_exibicao.append(nome_exib)
                self.turmas_map[nome_exib] = turma.id_turma
        
        self.cmb_turmas['values'] = nomes_turmas_exibicao
        if nomes_turmas_exibicao:
            self.cmb_turmas.current(0) # Aciona o trace
        else:
            self.id_turma_selecionada_var.set("") # Limpa para acionar trace e desabilitar
            messagebox.showinfo("Nenhuma Turma", "Você não está associado a nenhuma turma.", parent=self)

    def _ao_selecionar_turma(self, *args):
        self.atividades_map.clear()
        self.id_atividade_selecionada_var.set("")
        self.cmb_atividades.set("")
        self.cmb_atividades.config(state="disabled")
        self._limpar_e_resetar_lista_e_form()

        nome_exib_turma = self.id_turma_selecionada_var.get()
        id_turma_real = self.turmas_map.get(nome_exib_turma)

        if not id_turma_real:
            return

        atividades_obj: List['Atividade'] = self.app_controller.obter_atividades_por_turma(id_turma_real)
        nomes_atividades_exibicao = []
        if atividades_obj:
            for ativ in atividades_obj:
                nome_exib = f"{ativ.titulo} (Tipo: {ativ.tipo}) - ID: {ativ.id_atividade[:8]}"
                nomes_atividades_exibicao.append(nome_exib)
                self.atividades_map[nome_exib] = ativ.id_atividade
        
        self.cmb_atividades['values'] = nomes_atividades_exibicao
        if nomes_atividades_exibicao:
            self.cmb_atividades.config(state="readonly")
            self.cmb_atividades.current(0) # Aciona o trace
        else:
            messagebox.showinfo("Nenhuma Atividade", "Não há atividades cadastradas para esta turma.", parent=self)

    def _ao_selecionar_atividade(self, *args):
        self._limpar_e_resetar_lista_e_form() # Limpa antes de carregar novas notas
        self._carregar_alunos_e_avaliacoes_na_treeview()

    def _limpar_e_resetar_lista_e_form(self):
        for i in self.tree_alunos_notas.get_children():
            self.tree_alunos_notas.delete(i)
        self._limpar_formulario_avaliacao()


    def _carregar_alunos_e_avaliacoes_na_treeview(self):
        for i in self.tree_alunos_notas.get_children():
            self.tree_alunos_notas.delete(i)

        nome_exib_turma = self.id_turma_selecionada_var.get()
        id_turma_real = self.turmas_map.get(nome_exib_turma)
        nome_exib_atividade = self.id_atividade_selecionada_var.get()
        id_atividade_real = self.atividades_map.get(nome_exib_atividade)

        if not id_turma_real or not id_atividade_real:
            return

        alunos_da_turma: List['Aluno'] = self.app_controller.obter_alunos_da_turma(id_turma_real)
        avaliacoes_existentes: List['Avaliacao'] = self.app_controller.obter_avaliacoes_por_turma_e_atividade(id_turma_real, id_atividade_real)
        
        map_avaliacoes_por_aluno = {aval.id_aluno: aval for aval in avaliacoes_existentes}

        for aluno in alunos_da_turma:
            avaliacao_aluno = map_avaliacoes_por_aluno.get(aluno.id_usuario)
            nota = avaliacao_aluno.nota if avaliacao_aluno else "N/L" # Não Lançada
            feedback_resumido = avaliacao_aluno.feedback_professor[:30] + "..." if avaliacao_aluno and avaliacao_aluno.feedback_professor else ""
            id_avaliacao = avaliacao_aluno.id_avaliacao if avaliacao_aluno else None
            
            # Usar id_aluno como iid principal. Guardar id_avaliacao em tags se existir.
            self.tree_alunos_notas.insert("", tk.END, iid=aluno.id_usuario, 
                                        values=(aluno.nome, nota, feedback_resumido),
                                        tags=(id_avaliacao,) if id_avaliacao else ("nova_avaliacao",))
        
        self._limpar_formulario_avaliacao() # Garante que o form está pronto para nova entrada ou edição


    def _ao_selecionar_aluno_na_treeview(self, event=None):
        selecionado_iid = self.tree_alunos_notas.selection()
        if not selecionado_iid:
            self._limpar_formulario_avaliacao()
            return
        
        id_aluno_selecionado = selecionado_iid[0] # iid é o id_aluno
        item_selecionado = self.tree_alunos_notas.item(id_aluno_selecionado)
        tags = item_selecionado.get('tags')
        
        aluno_obj = self.app_controller.obter_aluno_por_id(id_aluno_selecionado)
        if not aluno_obj: return # Segurança

        self.id_aluno_form_var.set(aluno_obj.id_usuario)
        self.nome_aluno_form_var.set(aluno_obj.nome)
        
        self.ent_nota.config(state="normal")
        self.txt_feedback.config(state="normal")
        self.btn_salvar_avaliacao.config(state="normal")
        self.btn_limpar_form.config(state="normal")

        if tags and tags[0] != "nova_avaliacao":
            id_avaliacao_existente = tags[0]
            avaliacao_obj = self.app_controller.obter_avaliacao_por_id(id_avaliacao_existente)
            if avaliacao_obj:
                self.id_avaliacao_var.set(avaliacao_obj.id_avaliacao)
                self.nota_var.set(str(avaliacao_obj.nota))
                self.txt_feedback.delete("1.0", tk.END)
                self.txt_feedback.insert("1.0", avaliacao_obj.feedback_professor)
            else: # Avaliação marcada na tree mas não encontrada (erro de dados?)
                self.id_avaliacao_var.set("") # Indica nova avaliação
                self.nota_var.set("")
                self.txt_feedback.delete("1.0", tk.END)
        else: # Nova avaliação para este aluno
            self.id_avaliacao_var.set("") # Limpa ID, indicando que é uma nova avaliação
            self.nota_var.set("")
            self.txt_feedback.delete("1.0", tk.END)
        
        self.ent_nota.focus()


    def _limpar_formulario_avaliacao(self):
        self.id_avaliacao_var.set("")
        self.id_aluno_form_var.set("")
        self.nome_aluno_form_var.set("")
        self.nota_var.set("")
        self.txt_feedback.delete("1.0", tk.END)

        self.ent_nota.config(state="disabled")
        self.txt_feedback.config(state="disabled")
        self.btn_salvar_avaliacao.config(state="disabled")
        self.btn_limpar_form.config(state="disabled")

        if self.tree_alunos_notas.selection():
            self.tree_alunos_notas.selection_remove(self.tree_alunos_notas.selection())


    def _salvar_avaliacao(self):
        id_turma_real = self.turmas_map.get(self.id_turma_selecionada_var.get())
        id_atividade_real = self.atividades_map.get(self.id_atividade_selecionada_var.get())
        id_aluno_no_form = self.id_aluno_form_var.get()

        if not all([id_turma_real, id_atividade_real, id_aluno_no_form]):
            messagebox.showerror("Erro de Contexto", "Turma, Atividade e Aluno devem estar selecionados/definidos.", parent=self)
            return

        nota = self.nota_var.get().strip()
        feedback = self.txt_feedback.get("1.0", tk.END).strip()

        if not nota: # Feedback pode ser opcional
            messagebox.showerror("Validação", "O campo 'Nota' é obrigatório.", parent=self)
            return

        dados_avaliacao = {
            "id_aluno": id_aluno_no_form,
            "id_atividade": id_atividade_real,
            "id_turma": id_turma_real,
            "nota": nota,
            "feedback_professor": feedback,
            "id_professor_avaliador": self.id_professor_logado
        }

        id_avaliacao_existente = self.id_avaliacao_var.get()
        sucesso = False
        mensagem = ""

        if id_avaliacao_existente: # Edição
            sucesso, mensagem = self.app_controller.atualizar_avaliacao(id_avaliacao_existente, dados_avaliacao)
        else: # Nova
            dados_avaliacao["id_avaliacao"] = str(uuid.uuid4()) # Gerar ID para nova
            sucesso, mensagem = self.app_controller.criar_avaliacao(dados_avaliacao)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            self._carregar_alunos_e_avaliacoes_na_treeview() # Recarrega a lista
            # _limpar_formulario_avaliacao() é chamado dentro de _carregar_alunos_e_avaliacoes_na_treeview indiretamente
        else:
            messagebox.showerror("Erro ao Salvar", mensagem, parent=self)