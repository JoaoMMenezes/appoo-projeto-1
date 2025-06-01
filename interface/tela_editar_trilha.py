# interface/tela_editar_trilha.py
import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from typing import TYPE_CHECKING, List, Optional, Dict

if TYPE_CHECKING:
    from main import AppController
    from entidades.trilha import TrilhaAprendizagem
    from entidades.curso import Curso
    from entidades.atividade import Atividade

class DialogoAdicionarItemTrilha(tk.Toplevel):
    """Janela de diálogo para adicionar um novo item à sequência da trilha."""
    def __init__(self, master, app_controller: 'AppController', tipos_disponiveis: List[str]):
        super().__init__(master)
        self.app_controller = app_controller
        self.transient(master)
        self.grab_set()
        self.title("Adicionar Item à Trilha")
        self.geometry("500x300")

        self.resultado: Optional[Dict] = None # {"tipo": str, "id_item": str, "nome_referencia": str}

        self.tipo_item_var = tk.StringVar()
        self.item_selecionado_id_var = tk.StringVar() # Guarda o ID do curso/atividade
        self.nome_referencia_var = tk.StringVar()

        self.itens_map = {} # Mapeia nome de exibição para ID real

        self._configurar_interface_dialogo(tipos_disponiveis)
        self.tipo_item_var.trace_add("write", self._atualizar_combobox_itens)

    def _configurar_interface_dialogo(self, tipos_disponiveis: List[str]):
        frame = ttk.Frame(self, padding=10)
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Tipo de Item:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cmb_tipo_item = ttk.Combobox(frame, textvariable=self.tipo_item_var, values=tipos_disponiveis, state="readonly")
        self.cmb_tipo_item.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        if tipos_disponiveis:
            self.cmb_tipo_item.set(tipos_disponiveis[0])

        ttk.Label(frame, text="Selecionar Item Existente:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cmb_itens_existentes = ttk.Combobox(frame, textvariable=self.item_selecionado_id_var, state="readonly", width=40)
        self.cmb_itens_existentes.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.cmb_itens_existentes.bind("<<ComboboxSelected>>", self._preencher_nome_referencia_auto)


        ttk.Label(frame, text="Nome de Referência na Trilha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ent_nome_referencia = ttk.Entry(frame, textvariable=self.nome_referencia_var, width=43)
        self.ent_nome_referencia.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        frame_botoes = ttk.Frame(frame)
        frame_botoes.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame_botoes, text="Adicionar", command=self._confirmar_adicao).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=5)

        frame.columnconfigure(1, weight=1)
        self._atualizar_combobox_itens() # Carga inicial

    def _atualizar_combobox_itens(self, *args):
        tipo = self.tipo_item_var.get()
        self.itens_map.clear()
        self.item_selecionado_id_var.set("")
        self.nome_referencia_var.set("")
        nomes_exibicao = []

        if tipo == "Curso": # "aula" no JSON, mas "Curso" para o usuário
            cursos: List['Curso'] = self.app_controller.obter_cursos()
            for curso in cursos:
                nome_exib = f"{curso.nome_curso} (ID: {curso.id_curso[:8]})"
                nomes_exibicao.append(nome_exib)
                self.itens_map[nome_exib] = curso.id_curso
        elif tipo == "Atividade":
            atividades: List['Atividade'] = self.app_controller.atividades # Acessa a lista diretamente
            for ativ in atividades:
                # Para atividades, pode ser útil mostrar a turma se disponível
                turma_da_atividade = self.app_controller.obter_turma_por_id(ativ.id_turma_ou_curso)
                contexto_turma = f" (Turma: {turma_da_atividade.nome_turma})" if turma_da_atividade else ""
                nome_exib = f"{ativ.titulo}{contexto_turma} (ID: {ativ.id_atividade[:8]})"
                nomes_exibicao.append(nome_exib)
                self.itens_map[nome_exib] = ativ.id_atividade
        
        self.cmb_itens_existentes['values'] = nomes_exibicao
        if nomes_exibicao:
            self.cmb_itens_existentes.set(nomes_exibicao[0])
            self._preencher_nome_referencia_auto()


    def _preencher_nome_referencia_auto(self, *args):
        item_selecionado_exibicao = self.cmb_itens_existentes.get()
        id_real = self.itens_map.get(item_selecionado_exibicao)
        if not id_real: return

        tipo_item_usr = self.tipo_item_var.get() # "Curso" ou "Atividade"
        
        if tipo_item_usr == "Curso":
            curso = self.app_controller.obter_curso_por_id(id_real)
            if curso: self.nome_referencia_var.set(curso.nome_curso)
        elif tipo_item_usr == "Atividade":
            atividade = self.app_controller.obter_atividade_por_id(id_real)
            if atividade: self.nome_referencia_var.set(atividade.titulo)


    def _confirmar_adicao(self):
        tipo_item_usr = self.tipo_item_var.get() # "Curso" ou "Atividade"
        item_selecionado_exibicao = self.cmb_itens_existentes.get()
        nome_ref = self.nome_referencia_var.get().strip()

        if not tipo_item_usr or not item_selecionado_exibicao or not nome_ref:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
            return

        id_item_real = self.itens_map.get(item_selecionado_exibicao)
        if not id_item_real:
            messagebox.showerror("Erro", "Item selecionado inválido.", parent=self)
            return
            
        # Mapear de volta para o tipo esperado no JSON da trilha
        tipo_item_json = "curso" if tipo_item_usr == "Curso" else "atividade"

        self.resultado = {
            "tipo": tipo_item_json,
            "id_item": id_item_real,
            "nome_referencia": nome_ref
        }
        self.destroy()

class TelaEditarTrilha(tk.Toplevel):
    def __init__(self, master, app_controller: 'AppController'):
        super().__init__(master)
        self.app_controller = app_controller
        self.transient(master)
        self.grab_set()
        self.title("Editar Conteúdo da Trilha de Aprendizagem")
        self.geometry("900x700")

        self.trilha_selecionada_id_var = tk.StringVar()
        self.trilhas_map = {} # nome_exibicao -> id_trilha

        # Variáveis para edição dos dados da Trilha em si
        self.nome_trilha_var = tk.StringVar()
        self.publico_alvo_var = tk.StringVar()
        
        self.sequencia_itens_local: List[Dict] = [] # Cópia local para edição

        self._configurar_interface()
        self._carregar_trilhas_no_combobox()
        self.trilha_selecionada_id_var.trace_add("write", self._ao_selecionar_trilha)

    def _configurar_interface(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Seleção de Trilha ---
        frame_selecao_trilha = ttk.LabelFrame(main_frame, text="1. Selecione a Trilha para Editar", padding=10)
        frame_selecao_trilha.pack(fill=tk.X, pady=(0,10))
        ttk.Label(frame_selecao_trilha, text="Trilhas Disponíveis:").pack(side=tk.LEFT, padx=5)
        self.cmb_trilhas = ttk.Combobox(frame_selecao_trilha, textvariable=self.trilha_selecionada_id_var, state="readonly", width=70)
        self.cmb_trilhas.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # --- Detalhes da Trilha (Editáveis) ---
        frame_detalhes_trilha = ttk.LabelFrame(main_frame, text="2. Detalhes da Trilha", padding=10)
        frame_detalhes_trilha.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_detalhes_trilha, text="Nome da Trilha:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.ent_nome_trilha = ttk.Entry(frame_detalhes_trilha, textvariable=self.nome_trilha_var, width=50, state="disabled")
        self.ent_nome_trilha.grid(row=0, column=1, padx=5, pady=3, sticky="ew")

        ttk.Label(frame_detalhes_trilha, text="Descrição:").grid(row=1, column=0, padx=5, pady=3, sticky="nw")
        self.txt_descricao_trilha = tk.Text(frame_detalhes_trilha, height=3, width=50, state="disabled", wrap=tk.WORD)
        self.txt_descricao_trilha.grid(row=1, column=1, padx=5, pady=3, sticky="ew")
        scroll_desc = ttk.Scrollbar(frame_detalhes_trilha, orient=tk.VERTICAL, command=self.txt_descricao_trilha.yview)
        self.txt_descricao_trilha.config(yscrollcommand=scroll_desc.set)
        scroll_desc.grid(row=1, column=2, sticky="ns")


        ttk.Label(frame_detalhes_trilha, text="Público Alvo:").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.ent_publico_alvo = ttk.Entry(frame_detalhes_trilha, textvariable=self.publico_alvo_var, width=50, state="disabled")
        self.ent_publico_alvo.grid(row=2, column=1, padx=5, pady=3, sticky="ew")
        frame_detalhes_trilha.columnconfigure(1, weight=1)

        # --- Itens da Sequência ---
        frame_sequencia = ttk.LabelFrame(main_frame, text="3. Sequência de Itens da Trilha", padding=10)
        frame_sequencia.pack(fill=tk.BOTH, expand=True, pady=5)

        cols_itens = ("ordem", "tipo", "nome_ref", "id_item_display")
        self.tree_itens_trilha = ttk.Treeview(frame_sequencia, columns=cols_itens, show="headings", height=10, selectmode="browse")
        self.tree_itens_trilha.heading("ordem", text="#")
        self.tree_itens_trilha.heading("tipo", text="Tipo")
        self.tree_itens_trilha.heading("nome_ref", text="Nome de Referência")
        self.tree_itens_trilha.heading("id_item_display", text="ID do Item")
        self.tree_itens_trilha.column("ordem", width=40, anchor="center", stretch=tk.NO)
        self.tree_itens_trilha.column("tipo", width=100, anchor="center")
        self.tree_itens_trilha.column("nome_ref", width=300)
        self.tree_itens_trilha.column("id_item_display", width=200, stretch=tk.NO)
        
        scroll_tree_itens = ttk.Scrollbar(frame_sequencia, orient=tk.VERTICAL, command=self.tree_itens_trilha.yview)
        self.tree_itens_trilha.config(yscrollcommand=scroll_tree_itens.set)
        self.tree_itens_trilha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_tree_itens.pack(side=tk.RIGHT, fill=tk.Y)

        frame_botoes_itens = ttk.Frame(frame_sequencia)
        frame_botoes_itens.pack(fill=tk.X, pady=5)
        self.btn_adicionar_item = ttk.Button(frame_botoes_itens, text="Adicionar Item", command=self._abrir_dialogo_adicionar_item, state="disabled")
        self.btn_adicionar_item.pack(side=tk.LEFT, padx=5)
        self.btn_remover_item = ttk.Button(frame_botoes_itens, text="Remover Item Selecionado", command=self._remover_item_selecionado_da_sequencia, state="disabled")
        self.btn_remover_item.pack(side=tk.LEFT, padx=5)
        # Botões de reordenar podem ser adicionados aqui futuramente

        # --- Botões Finais ---
        frame_final = ttk.Frame(main_frame)
        frame_final.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        self.btn_salvar_trilha = ttk.Button(frame_final, text="Salvar Alterações na Trilha", command=self._salvar_alteracoes_trilha, state="disabled")
        self.btn_salvar_trilha.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_final, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        self._habilitar_campos_edicao_trilha(False)


    def _carregar_trilhas_no_combobox(self):
        trilhas: List['TrilhaAprendizagem'] = self.app_controller.obter_trilhas_disponiveis()
        self.trilhas_map.clear()
        nomes_exibicao = []
        for trilha in trilhas:
            nome_exib = f"{trilha.nome_trilha} (ID: {trilha.id_trilha[:8]})"
            nomes_exibicao.append(nome_exib)
            self.trilhas_map[nome_exib] = trilha.id_trilha
        
        self.cmb_trilhas['values'] = nomes_exibicao
        if nomes_exibicao:
            self.trilha_selecionada_id_var.set(nomes_exibicao[0]) # Aciona o _ao_selecionar_trilha
        else:
            self.trilha_selecionada_id_var.set("")
            messagebox.showinfo("Nenhuma Trilha", "Não há trilhas cadastradas para editar.", parent=self)

    def _habilitar_campos_edicao_trilha(self, habilitar: bool):
        estado = "normal" if habilitar else "disabled"
        self.ent_nome_trilha.config(state=estado)
        self.txt_descricao_trilha.config(state=estado)
        self.ent_publico_alvo.config(state=estado)
        self.btn_adicionar_item.config(state=estado)
        # self.btn_remover_item é habilitado na seleção de item
        self.btn_salvar_trilha.config(state=estado)


    def _ao_selecionar_trilha(self, *args):
        nome_exib_selecionado = self.trilha_selecionada_id_var.get()
        id_trilha_real = self.trilhas_map.get(nome_exib_selecionado)

        # Limpa campos e treeview antes de carregar novos dados ou se nenhuma trilha for válida
        self.nome_trilha_var.set("")
        self.txt_descricao_trilha.delete("1.0", tk.END)
        self.publico_alvo_var.set("")
        self.sequencia_itens_local = []
        for i in self.tree_itens_trilha.get_children():
            self.tree_itens_trilha.delete(i)
        self.btn_remover_item.config(state="disabled")

        if not id_trilha_real:
            self._habilitar_campos_edicao_trilha(False)
            return

        trilha_obj = self.app_controller.obter_trilha_por_id(id_trilha_real)
        if trilha_obj:
            self.nome_trilha_var.set(trilha_obj.nome_trilha)
            self.txt_descricao_trilha.insert("1.0", trilha_obj.descricao)
            self.publico_alvo_var.set(trilha_obj.publico_alvo)
            
            self.sequencia_itens_local = list(trilha_obj.sequencia_itens) # Cópia para edição local
            self._popular_treeview_itens_trilha()
            self._habilitar_campos_edicao_trilha(True)
        else:
            messagebox.showerror("Erro", "Trilha não encontrada.", parent=self)
            self._habilitar_campos_edicao_trilha(False)

    def _popular_treeview_itens_trilha(self):
        for i in self.tree_itens_trilha.get_children():
            self.tree_itens_trilha.delete(i)
        
        for idx, item in enumerate(self.sequencia_itens_local):
            tipo_usr = "Curso" if item.get("tipo") == "curso" else "Atividade"
            self.tree_itens_trilha.insert("", tk.END, values=(
                idx + 1,
                tipo_usr,
                item.get("nome_referencia", "N/A"),
                item.get("id_item", "N/A")[:15] + "..." # Mostra parte do ID
            ), iid=str(idx)) # Usar índice como IID para facilitar remoção/reordenação local
        
        # Habilitar/desabilitar botão de remover
        if self.tree_itens_trilha.selection():
            self.btn_remover_item.config(state="normal")
        else:
            self.btn_remover_item.config(state="disabled")
        # Lógica similar para botões de mover se implementados


    def _abrir_dialogo_adicionar_item(self):
        tipos_para_dialogo = ["Curso", "Atividade"] # Tipos que o usuário pode selecionar
        dialogo = DialogoAdicionarItemTrilha(self, self.app_controller, tipos_para_dialogo)
        self.wait_window(dialogo) # Espera o diálogo fechar

        if dialogo.resultado:
            self.sequencia_itens_local.append(dialogo.resultado)
            self._popular_treeview_itens_trilha()

    def _remover_item_selecionado_da_sequencia(self):
        selecionado = self.tree_itens_trilha.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um item da sequência para remover.", parent=self)
            return
        
        indice_selecionado = int(selecionado[0]) # IID é o índice
        if 0 <= indice_selecionado < len(self.sequencia_itens_local):
            del self.sequencia_itens_local[indice_selecionado]
            self._popular_treeview_itens_trilha()
        else:
            messagebox.showerror("Erro", "Índice do item selecionado é inválido.", parent=self)


    def _salvar_alteracoes_trilha(self):
        id_trilha_real = self.trilhas_map.get(self.trilha_selecionada_id_var.get())
        if not id_trilha_real:
            messagebox.showerror("Erro", "Nenhuma trilha selecionada para salvar.", parent=self)
            return

        novo_nome_trilha = self.nome_trilha_var.get().strip()
        nova_descricao = self.txt_descricao_trilha.get("1.0", tk.END).strip()
        novo_publico_alvo = self.publico_alvo_var.get().strip()

        if not novo_nome_trilha or not nova_descricao:
            messagebox.showerror("Validação", "Nome e Descrição da Trilha são obrigatórios.", parent=self)
            return

        novos_dados_trilha = {
            "nome_trilha": novo_nome_trilha,
            "descricao": nova_descricao,
            "publico_alvo": novo_publico_alvo
        }

        # A self.sequencia_itens_local já está atualizada
        sucesso, mensagem = self.app_controller.atualizar_dados_trilha(id_trilha_real, novos_dados_trilha, self.sequencia_itens_local)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            # Recarregar trilhas no combobox pode ser necessário se nomes mudaram
            # e resetar a seleção para forçar recarga dos dados da trilha
            idx_atual_combo = self.cmb_trilhas.current()
            self._carregar_trilhas_no_combobox()
            if idx_atual_combo != -1 and idx_atual_combo < len(self.cmb_trilhas['values']):
                 self.cmb_trilhas.current(idx_atual_combo) # Tenta manter a seleção
            else:
                self._ao_selecionar_trilha() # força recarga se a seleção sumiu
        else:
            messagebox.showerror("Erro ao Salvar", mensagem, parent=self)