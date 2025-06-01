# interface/tela_gerenciar_usuarios.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from main import AppController # Para type hinting
    from usuarios.usuario import Usuario # Para type hinting

class TelaGerenciarUsuarios(tk.Toplevel):
    """
    Tela para Coordenadores gerenciarem todos os usuários do sistema.
    """
    def __init__(self, master, app_controller: 'AppController'):
        super().__init__(master)
        self.app_controller = app_controller
        self.transient(master)
        self.grab_set()
        self.title("Gerenciar Usuários do Sistema")
        self.geometry("950x700") # Ajuste conforme necessário

        # Variáveis de controle para o formulário
        self.id_usuario_var = tk.StringVar()
        self.nome_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.tipo_usuario_form_var = tk.StringVar() # Para exibir o tipo no formulário

        # Variáveis para campos específicos (usadas para exibir/editar)
        self.matricula_var = tk.StringVar()
        self.departamento_var = tk.StringVar()
        self.area_coordenacao_var = tk.StringVar()

        self.usuario_selecionado_original_email = None # Para verificar mudança de email

        self._configurar_interface()
        self._carregar_usuarios_na_treeview()
        self._limpar_formulario()

    def _configurar_interface(self):
        # --- Frame principal ---
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Frame para formulário de edição ---
        frame_formulario = ttk.LabelFrame(main_frame, text="Detalhes do Usuário", padding=10)
        frame_formulario.pack(fill=tk.X, pady=5)

        ttk.Label(frame_formulario, text="ID Usuário:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_id_usuario = ttk.Entry(frame_formulario, textvariable=self.id_usuario_var, state="readonly", width=40)
        self.ent_id_usuario.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Nome Completo:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_nome = ttk.Entry(frame_formulario, textvariable=self.nome_var, width=40, state="disabled")
        self.ent_nome.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ent_email = ttk.Entry(frame_formulario, textvariable=self.email_var, width=40, state="disabled")
        self.ent_email.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Tipo de Usuário:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ent_tipo_usuario = ttk.Entry(frame_formulario, textvariable=self.tipo_usuario_form_var, state="readonly", width=40)
        self.ent_tipo_usuario.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        frame_formulario.columnconfigure(1, weight=1)

        # --- Frame para campos específicos (será atualizado dinamicamente) ---
        self.frame_especifico_form_container = ttk.Frame(main_frame, padding=(10,0))
        self.frame_especifico_form_container.pack(fill=tk.X, pady=5)
        self.frame_especifico_form_atual = None # Placeholder

        # --- Frame para botões de ação do formulário ---
        frame_botoes_form = ttk.Frame(main_frame)
        frame_botoes_form.pack(fill=tk.X, pady=10)

        self.btn_limpar_form = ttk.Button(frame_botoes_form, text="Limpar Seleção", command=self._limpar_formulario)
        self.btn_limpar_form.pack(side=tk.LEFT, padx=5)
        self.btn_salvar_alt = ttk.Button(frame_botoes_form, text="Salvar Alterações", command=self._salvar_alteracoes_usuario, state="disabled")
        self.btn_salvar_alt.pack(side=tk.LEFT, padx=5)

        # --- Frame para lista de usuários ---
        frame_lista = ttk.LabelFrame(main_frame, text="Usuários Cadastrados", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=5)

        colunas = ("id", "nome", "email", "tipo")
        self.tree_usuarios = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=15, selectmode="browse")
        self.tree_usuarios.heading("id", text="ID")
        self.tree_usuarios.heading("nome", text="Nome")
        self.tree_usuarios.heading("email", text="Email")
        self.tree_usuarios.heading("tipo", text="Tipo")

        self.tree_usuarios.column("id", width=220, minwidth=180, stretch=tk.NO)
        self.tree_usuarios.column("nome", width=200, minwidth=150)
        self.tree_usuarios.column("email", width=200, minwidth=150)
        self.tree_usuarios.column("tipo", width=100, minwidth=80, anchor="center")

        scrollbar_tree = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scrollbar_tree.set)
        self.tree_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._ao_selecionar_usuario)

        # --- Frame para botões globais da tela ---
        frame_botoes_tela = ttk.Frame(main_frame)
        frame_botoes_tela.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        self.btn_adicionar_novo = ttk.Button(frame_botoes_tela, text="Adicionar Novo Usuário", command=self._abrir_tela_cadastro_novo_usuario)
        self.btn_adicionar_novo.pack(side=tk.LEFT, padx=5)
        self.btn_excluir_sel = ttk.Button(frame_botoes_tela, text="Excluir Selecionado", command=self._excluir_usuario_selecionado, state="disabled")
        self.btn_excluir_sel.pack(side=tk.LEFT, padx=5)
        self.btn_fechar_tela = ttk.Button(frame_botoes_tela, text="Fechar Janela", command=self.destroy)
        self.btn_fechar_tela.pack(side=tk.RIGHT, padx=5)


    def _carregar_usuarios_na_treeview(self):
        for i in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(i)

        todos_usuarios: list['Usuario'] = self.app_controller.alunos + \
                                       self.app_controller.professores + \
                                       self.app_controller.coordenadores
        
        for usuario in todos_usuarios:
            self.tree_usuarios.insert("", tk.END, values=(
                usuario.id_usuario, usuario.nome, usuario.email, usuario.obter_tipo_usuario()
            ), iid=usuario.id_usuario)

    def _atualizar_campos_especificos_formulario(self, usuario: 'Usuario' = None):
        if self.frame_especifico_form_atual:
            self.frame_especifico_form_atual.destroy()
            self.frame_especifico_form_atual = None

        self.matricula_var.set("")
        self.departamento_var.set("")
        self.area_coordenacao_var.set("")
        
        estado_entry = "normal" if usuario else "disabled"

        if usuario:
            tipo_usuario = usuario.obter_tipo_usuario()
            if tipo_usuario == "Aluno":
                self.frame_especifico_form_atual = ttk.LabelFrame(self.frame_especifico_form_container, text="Detalhes do Aluno", padding=5)
                ttk.Label(self.frame_especifico_form_atual, text="Matrícula:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
                ent_matricula = ttk.Entry(self.frame_especifico_form_atual, textvariable=self.matricula_var, width=38, state=estado_entry)
                ent_matricula.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
                self.matricula_var.set(getattr(usuario, 'matricula', ''))
                self.frame_especifico_form_atual.columnconfigure(1, weight=1)
            elif tipo_usuario == "Professor":
                self.frame_especifico_form_atual = ttk.LabelFrame(self.frame_especifico_form_container, text="Detalhes do Professor", padding=5)
                ttk.Label(self.frame_especifico_form_atual, text="Departamento:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
                ent_departamento = ttk.Entry(self.frame_especifico_form_atual, textvariable=self.departamento_var, width=38, state=estado_entry)
                ent_departamento.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
                self.departamento_var.set(getattr(usuario, 'departamento', ''))
                self.frame_especifico_form_atual.columnconfigure(1, weight=1)
            elif tipo_usuario == "Coordenador":
                self.frame_especifico_form_atual = ttk.LabelFrame(self.frame_especifico_form_container, text="Detalhes do Coordenador", padding=5)
                ttk.Label(self.frame_especifico_form_atual, text="Área de Coordenação:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
                ent_area = ttk.Entry(self.frame_especifico_form_atual, textvariable=self.area_coordenacao_var, width=38, state=estado_entry)
                ent_area.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
                self.area_coordenacao_var.set(getattr(usuario, 'area_coordenacao', ''))
                self.frame_especifico_form_atual.columnconfigure(1, weight=1)
            
            if self.frame_especifico_form_atual:
                self.frame_especifico_form_atual.pack(fill=tk.X)

    def _ao_selecionar_usuario(self, event=None):
        selecionado_iid = self.tree_usuarios.selection()
        if not selecionado_iid:
            self._limpar_formulario()
            return

        id_usuario = selecionado_iid[0]
        usuario_obj = self.app_controller.obter_usuario_por_id_geral(id_usuario)

        if usuario_obj:
            self.id_usuario_var.set(usuario_obj.id_usuario)
            self.nome_var.set(usuario_obj.nome)
            self.email_var.set(usuario_obj.email)
            self.tipo_usuario_form_var.set(usuario_obj.obter_tipo_usuario())
            
            self.usuario_selecionado_original_email = usuario_obj.email # Guardar email original

            self._atualizar_campos_especificos_formulario(usuario_obj)

            self.ent_nome.config(state="normal")
            self.ent_email.config(state="normal")
            # Campos específicos já são configurados em _atualizar_campos_especificos_formulario
            self.btn_salvar_alt.config(state="normal")
            self.btn_excluir_sel.config(state="normal")
            self.ent_nome.focus()
        else:
            messagebox.showerror("Erro", f"Usuário com ID {id_usuario} não encontrado.", parent=self)
            self._limpar_formulario()

    def _limpar_formulario(self):
        self.id_usuario_var.set("")
        self.nome_var.set("")
        self.email_var.set("")
        self.tipo_usuario_form_var.set("")
        self.usuario_selecionado_original_email = None

        self._atualizar_campos_especificos_formulario(None) # Limpa e oculta campos específicos

        self.ent_nome.config(state="disabled")
        self.ent_email.config(state="disabled")
        self.btn_salvar_alt.config(state="disabled")
        self.btn_excluir_sel.config(state="disabled")

        if self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(self.tree_usuarios.selection())
        # Não focar em nada específico, pois o formulário está desabilitado

    def _salvar_alteracoes_usuario(self):
        id_usuario_alvo = self.id_usuario_var.get()
        if not id_usuario_alvo:
            messagebox.showerror("Erro", "Nenhum usuário selecionado para atualizar.", parent=self)
            return

        novo_nome = self.nome_var.get().strip()
        novo_email = self.email_var.get().strip()
        # Tipo de usuário não é editável aqui para simplificar
        tipo_usuario = self.tipo_usuario_form_var.get()

        if not novo_nome or not novo_email:
            messagebox.showerror("Validação", "Nome e Email não podem ser vazios.", parent=self)
            return

        novos_dados = {
            "nome": novo_nome,
            "email": novo_email
            # Não incluímos "senha" aqui, pois não estamos alterando a senha nesta tela.
        }

        # Coleta dados específicos atualizados
        if tipo_usuario == "Aluno":
            matricula = self.matricula_var.get().strip()
            if not matricula:
                messagebox.showerror("Validação", "Matrícula é obrigatória para Aluno.", parent=self)
                return
            novos_dados["matricula"] = matricula
        elif tipo_usuario == "Professor":
            departamento = self.departamento_var.get().strip()
            if not departamento:
                messagebox.showerror("Validação", "Departamento é obrigatório para Professor.", parent=self)
                return
            novos_dados["departamento"] = departamento
        elif tipo_usuario == "Coordenador":
            area_coordenacao = self.area_coordenacao_var.get().strip()
            if not area_coordenacao:
                messagebox.showerror("Validação", "Área de Coordenação é obrigatória.", parent=self)
                return
            novos_dados["area_coordenacao"] = area_coordenacao
        
        # Passa o email original para o controller poder verificar se houve mudança
        # e se o novo email já existe (caso tenha mudado).
        sucesso, mensagem = self.app_controller.atualizar_usuario(
            id_usuario_alvo, 
            novos_dados, 
            self.usuario_selecionado_original_email
        )

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            self._carregar_usuarios_na_treeview()
            self._limpar_formulario()
        else:
            messagebox.showerror("Erro ao Atualizar", mensagem, parent=self)

    def _excluir_usuario_selecionado(self):
        id_usuario_alvo = self.id_usuario_var.get()
        if not id_usuario_alvo:
            messagebox.showerror("Erro", "Nenhum usuário selecionado para excluir.", parent=self)
            return
        
        usuario_obj = self.app_controller.obter_usuario_por_id_geral(id_usuario_alvo)
        if not usuario_obj: # Segurança
            messagebox.showerror("Erro", "Usuário não encontrado.", parent=self)
            self._limpar_formulario()
            return

        if messagebox.askyesno("Confirmar Exclusão",
                               f"Tem certeza que deseja excluir o usuário:\n"
                               f"Nome: {usuario_obj.nome}\n"
                               f"Email: {usuario_obj.email}\n"
                               f"Tipo: {usuario_obj.obter_tipo_usuario()}\n\n"
                               f"Atenção: Esta ação é irreversível. Verifique se o usuário não possui "
                               f"vínculos importantes (ex: professor em turmas ativas) antes de prosseguir.",
                               icon='warning', parent=self):
            
            sucesso, mensagem = self.app_controller.excluir_usuario(id_usuario_alvo)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem, parent=self)
                self._carregar_usuarios_na_treeview()
                self._limpar_formulario()
            else:
                messagebox.showerror("Erro ao Excluir", mensagem, parent=self)

    def _abrir_tela_cadastro_novo_usuario(self):
        # Chama o método do AppController que abre a TelaCadastroUsuario
        self.app_controller.mostrar_tela_cadastro()
        # Opcional: recarregar a lista de usuários após o fechamento da tela de cadastro,
        # mas isso exigiria que a tela de cadastro sinalizasse de alguma forma.
        # Por simplicidade, o usuário pode ter que fechar e reabrir esta tela, ou podemos adicionar um botão "Atualizar Lista".
        # Ou, se a TelaCadastroUsuario for modal, podemos recarregar após ela fechar.
        # Como ela é um Toplevel com grab_set(), o fluxo para aqui até ela ser fechada.
        self.after(100, self._carregar_usuarios_na_treeview) # Recarrega após um pequeno delay