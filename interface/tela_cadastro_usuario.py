# interface/tela_cadastro_usuario.py
import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from main import AppController # Para type hinting

class TelaCadastroUsuario(tk.Toplevel):
    """
    Tela para cadastro de novos usuários (Alunos, Professores, Coordenadores).
    """
    def __init__(self, master, app_controller: 'AppController'):
        super().__init__(master)
        self.app_controller = app_controller
        self.transient(master)
        self.grab_set()
        self.title("Cadastrar Novo Usuário")
        self.geometry("550x550") # Ajuste conforme necessário

        # Variáveis de controle
        self.nome_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.senha_var = tk.StringVar()
        self.confirma_senha_var = tk.StringVar()
        self.tipo_usuario_var = tk.StringVar()

        # Variáveis para campos específicos
        self.matricula_var = tk.StringVar() # Aluno
        self.departamento_var = tk.StringVar() # Professor
        self.area_coordenacao_var = tk.StringVar() # Coordenador

        self._configurar_interface()
        self._limpar_formulario() # Define valores iniciais e foca no primeiro campo

    def _configurar_interface(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Frame para dados comuns ---
        frame_comum = ttk.LabelFrame(main_frame, text="Dados Comuns", padding=10)
        frame_comum.pack(fill=tk.X, pady=5)

        ttk.Label(frame_comum, text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_nome = ttk.Entry(frame_comum, textvariable=self.nome_var, width=40)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_comum, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_email = ttk.Entry(frame_comum, textvariable=self.email_var, width=40)
        self.ent_email.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_comum, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ent_senha = ttk.Entry(frame_comum, textvariable=self.senha_var, show="*", width=40)
        self.ent_senha.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_comum, text="Confirmar Senha:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ent_confirma_senha = ttk.Entry(frame_comum, textvariable=self.confirma_senha_var, show="*", width=40)
        self.ent_confirma_senha.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_comum, text="Tipo de Usuário:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.cmb_tipo_usuario = ttk.Combobox(frame_comum, textvariable=self.tipo_usuario_var,
                                             values=["Aluno", "Professor", "Coordenador"], state="readonly", width=38)
        self.cmb_tipo_usuario.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.cmb_tipo_usuario.bind("<<ComboboxSelected>>", self._atualizar_campos_especificos)

        frame_comum.columnconfigure(1, weight=1)

        # --- Frame para dados específicos (será atualizado dinamicamente) ---
        self.frame_especifico_container = ttk.Frame(main_frame, padding=10)
        self.frame_especifico_container.pack(fill=tk.X, pady=5)
        self.frame_especifico_atual = None # Placeholder para o frame do tipo de usuário

        # --- Botões de Ação ---
        frame_botoes = ttk.Frame(main_frame, padding=(0, 10))
        frame_botoes.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        self.btn_salvar = ttk.Button(frame_botoes, text="Salvar Cadastro", command=self._salvar_cadastro)
        self.btn_salvar.pack(side=tk.LEFT, padx=10, expand=True)

        self.btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self._limpar_formulario)
        self.btn_limpar.pack(side=tk.LEFT, padx=10, expand=True)

        self.btn_fechar = ttk.Button(frame_botoes, text="Fechar", command=self.destroy)
        self.btn_fechar.pack(side=tk.RIGHT, padx=10, expand=True)


    def _atualizar_campos_especificos(self, event=None):
        tipo_selecionado = self.tipo_usuario_var.get()

        if self.frame_especifico_atual:
            self.frame_especifico_atual.destroy()
            self.frame_especifico_atual = None

        if tipo_selecionado == "Aluno":
            self.frame_especifico_atual = ttk.LabelFrame(self.frame_especifico_container, text="Dados do Aluno", padding=10)
            ttk.Label(self.frame_especifico_atual, text="Matrícula:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            ent_matricula = ttk.Entry(self.frame_especifico_atual, textvariable=self.matricula_var, width=38)
            ent_matricula.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.frame_especifico_atual.columnconfigure(1, weight=1)
            self.frame_especifico_atual.pack(fill=tk.X)
            ent_matricula.focus()
        elif tipo_selecionado == "Professor":
            self.frame_especifico_atual = ttk.LabelFrame(self.frame_especifico_container, text="Dados do Professor", padding=10)
            ttk.Label(self.frame_especifico_atual, text="Departamento:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            ent_departamento = ttk.Entry(self.frame_especifico_atual, textvariable=self.departamento_var, width=38)
            ent_departamento.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.frame_especifico_atual.columnconfigure(1, weight=1)
            self.frame_especifico_atual.pack(fill=tk.X)
            ent_departamento.focus()
        elif tipo_selecionado == "Coordenador":
            self.frame_especifico_atual = ttk.LabelFrame(self.frame_especifico_container, text="Dados do Coordenador", padding=10)
            ttk.Label(self.frame_especifico_atual, text="Área de Coordenação:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            ent_area_coordenacao = ttk.Entry(self.frame_especifico_atual, textvariable=self.area_coordenacao_var, width=38)
            ent_area_coordenacao.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.frame_especifico_atual.columnconfigure(1, weight=1)
            self.frame_especifico_atual.pack(fill=tk.X)
            ent_area_coordenacao.focus()

    def _limpar_formulario(self):
        self.nome_var.set("")
        self.email_var.set("")
        self.senha_var.set("")
        self.confirma_senha_var.set("")
        self.tipo_usuario_var.set("") # Limpa a seleção do combobox
        self.matricula_var.set("")
        self.departamento_var.set("")
        self.area_coordenacao_var.set("")

        if self.frame_especifico_atual:
            self.frame_especifico_atual.destroy()
            self.frame_especifico_atual = None

        self.ent_nome.focus()

    def _salvar_cadastro(self):
        nome = self.nome_var.get().strip()
        email = self.email_var.get().strip()
        senha = self.senha_var.get() # Não usa strip em senha
        confirma_senha = self.confirma_senha_var.get()
        tipo_usuario = self.tipo_usuario_var.get()

        # Validações básicas
        if not all([nome, email, senha, confirma_senha, tipo_usuario]):
            messagebox.showerror("Erro de Validação", "Todos os campos comuns são obrigatórios.", parent=self)
            return

        if senha != confirma_senha:
            messagebox.showerror("Erro de Validação", "As senhas não coincidem.", parent=self)
            self.senha_var.set("")
            self.confirma_senha_var.set("")
            self.ent_senha.focus()
            return

        # Coleta dados específicos
        dados_especificos = {}
        if tipo_usuario == "Aluno":
            matricula = self.matricula_var.get().strip()
            if not matricula:
                messagebox.showerror("Erro de Validação", "Matrícula é obrigatória para Aluno.", parent=self)
                return
            dados_especificos["matricula"] = matricula
        elif tipo_usuario == "Professor":
            departamento = self.departamento_var.get().strip()
            if not departamento:
                messagebox.showerror("Erro de Validação", "Departamento é obrigatório para Professor.", parent=self)
                return
            dados_especificos["departamento"] = departamento
        elif tipo_usuario == "Coordenador":
            area_coordenacao = self.area_coordenacao_var.get().strip()
            if not area_coordenacao:
                messagebox.showerror("Erro de Validação", "Área de Coordenação é obrigatória para Coordenador.", parent=self)
                return
            dados_especificos["area_coordenacao"] = area_coordenacao

        # Prepara dados para enviar ao controller
        dados_cadastro = {
            "id_usuario": str(uuid.uuid4()), # O controller pode gerar ou usar este
            "nome": nome,
            "email": email,
            "senha": senha, # A classe Usuario fará o hash
            "tipo_usuario": tipo_usuario,
            **dados_especificos
        }

        sucesso, mensagem = self.app_controller.cadastrar_novo_usuario(dados_cadastro)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            self._limpar_formulario()
        else:
            messagebox.showerror("Erro no Cadastro", mensagem, parent=self)

# Exemplo de como usar esta tela (para teste, seria chamado pelo AppController)
if __name__ == '__main__':
    class MockAppController:
        def cadastrar_novo_usuario(self, dados_usuario: dict) -> Tuple[bool, str]:
            print("Tentativa de cadastro com os seguintes dados:")
            print(dados_usuario)
            # Simular verificação de email
            if dados_usuario["email"] == "existente@email.com":
                return False, f"Email '{dados_usuario['email']}' já cadastrado."
            
            # Simular sucesso
            # Aqui você adicionaria o usuário às listas e salvaria os dados
            return True, f"Usuário '{dados_usuario['nome']}' ({dados_usuario['tipo_usuario']}) cadastrado com sucesso!"

    root = tk.Tk()
    root.withdraw() # Esconde a janela root principal para o teste da Toplevel
    mock_controller = MockAppController()
    tela_cadastro = TelaCadastroUsuario(root, mock_controller)
    tela_cadastro.protocol("WM_DELETE_WINDOW", root.destroy) # Fecha a aplicação ao fechar a janela
    root.mainloop()