# interface/tela_gerenciar_atividades_turma.py
import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from tkcalendar import DateEntry # Para seleção de data
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from main import AppController
    from entidades.turma import Turma
    from entidades.atividade import Atividade

class TelaGerenciarAtividadesTurma(tk.Toplevel):
    """
    Tela para professores gerenciarem atividades de suas turmas.
    """
    def __init__(self, master, app_controller: 'AppController', id_professor_logado: str):
        super().__init__(master)
        self.app_controller = app_controller
        self.id_professor_logado = id_professor_logado
        
        self.transient(master)
        self.grab_set()
        self.title("Gerenciar Atividades da Turma")
        self.geometry("900x700")

        # Variáveis de controle
        self.id_turma_selecionada_var = tk.StringVar()
        self.id_atividade_var = tk.StringVar()
        self.titulo_atividade_var = tk.StringVar()
        self.tipo_atividade_var = tk.StringVar()
        self.data_prazo_var = tk.StringVar() # DateEntry cuidará do formato

        self.turmas_professor_map = {} # nome_turma -> id_turma

        self._configurar_interface()
        self._carregar_turmas_do_professor()
        
        # Listener para quando uma turma é selecionada
        self.id_turma_selecionada_var.trace_add("write", self._ao_selecionar_turma_combobox)

    def _configurar_interface(self):
        # Frame principal
        frame_principal = ttk.Frame(self, padding=10)
        frame_principal.pack(expand=True, fill=tk.BOTH)

        # --- Seleção de Turma ---
        frame_selecao_turma = ttk.LabelFrame(frame_principal, text="Selecionar Turma", padding=10)
        frame_selecao_turma.pack(fill=tk.X, pady=(0,10))

        ttk.Label(frame_selecao_turma, text="Minhas Turmas:").pack(side=tk.LEFT, padx=5)
        self.cmb_turmas = ttk.Combobox(frame_selecao_turma, textvariable=self.id_turma_selecionada_var, state="readonly", width=40)
        self.cmb_turmas.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # --- Formulário de Atividade ---
        frame_formulario = ttk.LabelFrame(frame_principal, text="Detalhes da Atividade", padding=10)
        frame_formulario.pack(fill=tk.X, pady=(0,10))

        ttk.Label(frame_formulario, text="ID Atividade:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_id_atividade = ttk.Entry(frame_formulario, textvariable=self.id_atividade_var, state="readonly", width=35)
        self.ent_id_atividade.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Título:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_titulo_atividade = ttk.Entry(frame_formulario, textvariable=self.titulo_atividade_var, width=35)
        self.ent_titulo_atividade.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Tipo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.cmb_tipo_atividade = ttk.Combobox(frame_formulario, textvariable=self.tipo_atividade_var, 
                                               values=["Prova", "Trabalho", "Exercício", "Apresentação", "Outro"], 
                                               state="readonly", width=33)
        self.cmb_tipo_atividade.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.cmb_tipo_atividade.set("Trabalho") # Padrão

        ttk.Label(frame_formulario, text="Data de Prazo:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        # Usando tkcalendar.DateEntry para um seletor de data
        self.cal_data_prazo = DateEntry(frame_formulario, width=12, background='darkblue', foreground='white', 
                                        borderwidth=2, date_pattern='dd/mm/yyyy', textvariable=self.data_prazo_var)
        self.cal_data_prazo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.data_prazo_var.set("") # Limpa inicialmente


        ttk.Label(frame_formulario, text="Descrição:").grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        self.txt_descricao_atividade = tk.Text(frame_formulario, height=4, width=35)
        self.txt_descricao_atividade.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        scrollbar_desc = ttk.Scrollbar(frame_formulario, orient="vertical", command=self.txt_descricao_atividade.yview)
        self.txt_descricao_atividade.configure(yscrollcommand=scrollbar_desc.set)
        scrollbar_desc.grid(row=4, column=2, sticky="ns")

        frame_formulario.columnconfigure(1, weight=1)

        # --- Botões de Ação do Formulário ---
        frame_botoes_form = ttk.Frame(frame_principal)
        frame_botoes_form.pack(fill=tk.X, pady=5)

        self.btn_nova_atividade = ttk.Button(frame_botoes_form, text="Nova/Limpar", command=self._limpar_formulario_atividade, state="disabled")
        self.btn_nova_atividade.pack(side=tk.LEFT, padx=5)
        self.btn_salvar_atividade = ttk.Button(frame_botoes_form, text="Salvar Atividade", command=self._salvar_atividade, state="disabled")
        self.btn_salvar_atividade.pack(side=tk.LEFT, padx=5)
        self.btn_excluir_atividade = ttk.Button(frame_botoes_form, text="Excluir Selecionada", command=self._excluir_atividade, state="disabled")
        self.btn_excluir_atividade.pack(side=tk.LEFT, padx=5)

        # --- Lista de Atividades da Turma Selecionada ---
        frame_lista_atividades = ttk.LabelFrame(frame_principal, text="Atividades da Turma", padding=10)
        frame_lista_atividades.pack(fill=tk.BOTH, expand=True, pady=(10,0))

        colunas_atividades = ("titulo", "tipo", "data_prazo")
        self.tree_atividades = ttk.Treeview(frame_lista_atividades, columns=colunas_atividades, show="headings", height=8, selectmode="browse")
        self.tree_atividades.heading("titulo", text="Título")
        self.tree_atividades.heading("tipo", text="Tipo")
        self.tree_atividades.heading("data_prazo", text="Prazo")

        self.tree_atividades.column("titulo", width=250, minwidth=200)
        self.tree_atividades.column("tipo", width=100, minwidth=80, anchor="center")
        self.tree_atividades.column("data_prazo", width=100, minwidth=80, anchor="center")

        scrollbar_atividades = ttk.Scrollbar(frame_lista_atividades, orient="vertical", command=self.tree_atividades.yview)
        self.tree_atividades.configure(yscrollcommand=scrollbar_atividades.set)
        self.tree_atividades.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_atividades.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_atividades.bind("<<TreeviewSelect>>", self._ao_selecionar_atividade_treeview)

        # Botão Fechar Janela
        btn_fechar_janela = ttk.Button(frame_principal, text="Fechar Janela", command=self.destroy)
        btn_fechar_janela.pack(pady=10, side=tk.BOTTOM)

        self._limpar_formulario_atividade() # Prepara o formulário

    def _carregar_turmas_do_professor(self):
        """Carrega as turmas que o professor logado leciona."""
        turmas_obj: List['Turma'] = self.app_controller.obter_turmas_por_professor(self.id_professor_logado)
        nomes_turmas = []
        self.turmas_professor_map.clear()
        if turmas_obj:
            for turma in turmas_obj:
                curso = self.app_controller.obter_curso_por_id(turma.id_curso)
                nome_exibicao = f"{turma.nome_turma} ({curso.nome_curso if curso else 'Curso Desconhecido'})"
                nomes_turmas.append(nome_exibicao)
                self.turmas_professor_map[nome_exibicao] = turma.id_turma
        
        self.cmb_turmas['values'] = nomes_turmas
        if nomes_turmas:
            self.id_turma_selecionada_var.set(nomes_turmas[0]) # Seleciona a primeira
            self._habilitar_controles_atividade(True)
        else:
            self.id_turma_selecionada_var.set("")
            messagebox.showinfo("Nenhuma Turma", "Você não está associado a nenhuma turma para gerenciar atividades.", parent=self)
            self._habilitar_controles_atividade(False)
        
        self._carregar_atividades_da_turma_selecionada() # Carrega atividades da primeira turma (se houver)


    def _ao_selecionar_turma_combobox(self, *args):
        """Chamado quando uma turma é selecionada no ComboBox."""
        self._carregar_atividades_da_turma_selecionada()
        self._limpar_formulario_atividade() # Limpa para evitar confusão de dados
        self._habilitar_controles_atividade(bool(self.id_turma_selecionada_var.get()))


    def _carregar_atividades_da_turma_selecionada(self):
        """Carrega e exibe as atividades da turma atualmente selecionada."""
        for i in self.tree_atividades.get_children():
            self.tree_atividades.delete(i)
        
        nome_turma_selecionada_exibicao = self.id_turma_selecionada_var.get()
        id_turma_real = self.turmas_professor_map.get(nome_turma_selecionada_exibicao)

        if not id_turma_real:
            self.btn_nova_atividade.config(state="disabled")
            return

        self.btn_nova_atividade.config(state="normal")
        atividades: List['Atividade'] = self.app_controller.obter_atividades_por_turma(id_turma_real)
        for ativ in atividades:
            self.tree_atividades.insert("", tk.END, values=(ativ.titulo, ativ.tipo, ativ.data_prazo), iid=ativ.id_atividade)

    def _limpar_formulario_atividade(self):
        """Limpa os campos do formulário de atividade."""
        self.id_atividade_var.set(str(uuid.uuid4())) # Novo ID para potencial nova atividade
        self.titulo_atividade_var.set("")
        self.txt_descricao_atividade.delete("1.0", tk.END)
        self.tipo_atividade_var.set("Trabalho") # Valor padrão
        self.data_prazo_var.set("") # Limpa o DateEntry
        self.cal_data_prazo.set_date(None) # Reseta o DateEntry visualmente
        self.ent_titulo_atividade.focus()
        self.btn_excluir_atividade.config(state="disabled")
        if self.tree_atividades.selection():
            self.tree_atividades.selection_remove(self.tree_atividades.selection())

    def _ao_selecionar_atividade_treeview(self, event=None):
        """Preenche o formulário quando uma atividade é selecionada na Treeview."""
        selecionado = self.tree_atividades.selection()
        if not selecionado:
            self.btn_excluir_atividade.config(state="disabled")
            return

        id_atividade_selecionada = selecionado[0] # O iid é o id_atividade
        nome_turma_selecionada_exibicao = self.id_turma_selecionada_var.get()
        id_turma_real = self.turmas_professor_map.get(nome_turma_selecionada_exibicao)

        if not id_turma_real: return

        atividade = self.app_controller.obter_atividade_por_id(id_atividade_selecionada)

        if atividade and atividade.id_turma_ou_curso == id_turma_real : # Garante que a atividade é da turma certa
            self.id_atividade_var.set(atividade.id_atividade)
            self.titulo_atividade_var.set(atividade.titulo)
            self.txt_descricao_atividade.delete("1.0", tk.END)
            self.txt_descricao_atividade.insert("1.0", atividade.descricao)
            self.tipo_atividade_var.set(atividade.tipo)
            self.data_prazo_var.set(atividade.data_prazo) # DateEntry deve atualizar
            self.cal_data_prazo.set_date(atividade.data_prazo) # Tentar formatar se necessário
            self.btn_excluir_atividade.config(state="normal")
        else:
            messagebox.showerror("Erro", f"Atividade com ID {id_atividade_selecionada} não encontrada ou não pertence a esta turma.", parent=self)
            self._limpar_formulario_atividade()


    def _habilitar_controles_atividade(self, habilitar: bool):
        """Habilita ou desabilita os controles do formulário de atividade."""
        estado = "normal" if habilitar else "disabled"
        self.ent_titulo_atividade.config(state=estado)
        self.cmb_tipo_atividade.config(state="readonly" if habilitar else "disabled") # readonly é o normal para combobox
        self.cal_data_prazo.config(state=estado)
        self.txt_descricao_atividade.config(state=estado)
        self.btn_nova_atividade.config(state=estado)
        self.btn_salvar_atividade.config(state=estado)
        # Excluir só habilita se algo estiver selecionado na treeview
        if not habilitar:
            self.btn_excluir_atividade.config(state="disabled")


    def _salvar_atividade(self):
        """Salva uma nova atividade ou atualiza uma existente."""
        nome_turma_selecionada_exibicao = self.id_turma_selecionada_var.get()
        id_turma_real = self.turmas_professor_map.get(nome_turma_selecionada_exibicao)

        if not id_turma_real:
            messagebox.showerror("Erro", "Nenhuma turma selecionada para salvar a atividade.", parent=self)
            return

        id_atividade = self.id_atividade_var.get()
        titulo = self.titulo_atividade_var.get().strip()
        descricao = self.txt_descricao_atividade.get("1.0", tk.END).strip()
        tipo = self.tipo_atividade_var.get()
        data_prazo = self.data_prazo_var.get() # DateEntry já formata como dd/mm/yyyy

        if not titulo or not tipo or not data_prazo or not descricao:
            messagebox.showerror("Validação", "Título, tipo, data de prazo e descrição são obrigatórios.", parent=self)
            return

        # Verifica se é uma atualização ou novo
        atividade_existente = self.app_controller.obter_atividade_por_id(id_atividade)
        
        if atividade_existente and atividade_existente.id_turma_ou_curso == id_turma_real: # Atualização
            sucesso, msg = self.app_controller.atualizar_atividade(id_atividade, id_turma_real, titulo, descricao, data_prazo, tipo)
        else: # Novo (ou ID foi limpo, então é novo)
            sucesso, msg = self.app_controller.criar_atividade(id_turma_real, titulo, descricao, data_prazo, tipo, id_atividade_manual=id_atividade)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self._carregar_atividades_da_turma_selecionada()
            self._limpar_formulario_atividade()
        else:
            messagebox.showerror("Erro ao Salvar", msg, parent=self)


    def _excluir_atividade(self):
        """Exclui a atividade selecionada."""
        selecionado = self.tree_atividades.selection()
        if not selecionado:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma atividade para excluir.", parent=self)
            return
        
        id_atividade_para_excluir = selecionado[0]
        
        # Adicionar verificação se há avaliações ligadas a esta atividade antes de excluir
        if self.app_controller.verificar_avaliacoes_para_atividade(id_atividade_para_excluir):
             if not messagebox.askyesno("Confirmar Exclusão", 
                                 f"Atenção: Existem avaliações (notas) lançadas para esta atividade. Excluir a atividade também removerá estas avaliações.\n\nDeseja continuar?",
                                 icon='warning', parent=self):
                return


        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir a atividade ID: {id_atividade_para_excluir}?", parent=self):
            sucesso, msg = self.app_controller.excluir_atividade(id_atividade_para_excluir)
            if sucesso:
                messagebox.showinfo("Sucesso", msg, parent=self)
                self._carregar_atividades_da_turma_selecionada()
                self._limpar_formulario_atividade()
            else:
                messagebox.showerror("Erro ao Excluir", msg, parent=self)