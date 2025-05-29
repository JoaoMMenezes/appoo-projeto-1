# interface/tela_login.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable # Para type hinting da função de callback

# Importações de classes do projeto (ajustar caminhos se necessário)
# from persistencia.gerenciador_dados import GerenciadorDados
# from usuarios.aluno import Aluno
# from usuarios.professor import Professor
# from usuarios.coordenador import Coordenador

class TelaLogin(ttk.Frame):
    """
    Tela de login da aplicação.
    Permite que o usuário insira email e senha para autenticação.
    """

    def __init__(self, container: tk.Tk | ttk.Frame, app_controller):
        """
        Construtor da TelaLogin.

        Args:
            container: O widget pai onde este frame será colocado.
            app_controller: Uma instância do controlador principal da aplicação,
                            que lidará com a lógica de login e navegação.
        """
        super().__init__(container)
        self.container = container
        self.app_controller = app_controller # Controlador da aplicação

        self.grid(row=0, column=0, sticky="nsew") # Faz o frame ocupar o espaço do container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Configuração do estilo (opcional, mas melhora a aparência)
        style = ttk.Style(self)
        style.configure("TLabel", padding=5, font=('Helvetica', 10))
        style.configure("TButton", padding=5, font=('Helvetica', 10))
        style.configure("TEntry", padding=5, font=('Helvetica', 10))

        # --- Widgets ---
        self.lbl_titulo = ttk.Label(self, text="Login do Sistema Educacional", font=('Helvetica', 16, 'bold'))
        self.lbl_email = ttk.Label(self, text="Email:")
        self.ent_email = ttk.Entry(self, width=30)
        self.lbl_senha = ttk.Label(self, text="Senha:")
        self.ent_senha = ttk.Entry(self, width=30, show="*")
        
        # Frame para os botões para melhor agrupamento
        frame_botoes = ttk.Frame(self) # frame_botoes é filho de self (TelaLogin)

        # Botões são filhos de frame_botoes
        self.btn_login = ttk.Button(frame_botoes, text="Login", command=self._realizar_login)
        self.btn_cadastrar = ttk.Button(frame_botoes, text="Criar Cadastro", command=self._abrir_cadastro)

        # --- Layout usando Grid para os elementos principais de TelaLogin ---
        # Centralizar o conteúdo de TelaLogin
        self.columnconfigure(0, weight=1) 
        self.columnconfigure(1, weight=1) 
        self.columnconfigure(2, weight=1) 

        # Posicionamento dos widgets principais em TelaLogin
        self.lbl_titulo.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")

        self.lbl_email.grid(row=1, column=0, padx=(10,0), pady=5, sticky="e")
        self.ent_email.grid(row=1, column=1, padx=(0,10), pady=5, sticky="ew")

        self.lbl_senha.grid(row=2, column=0, padx=(10,0), pady=5, sticky="e")
        self.ent_senha.grid(row=2, column=1, padx=(0,10), pady=5, sticky="ew")
        
        # Posicionamento do frame_botoes em TelaLogin (usando grid)
        frame_botoes.grid(row=3, column=0, columnspan=3, pady=15, sticky="n")
        # Configurar colunas dentro de frame_botoes para centralizar os botões se necessário
        # frame_botoes.columnconfigure(0, weight=1) 
        # frame_botoes.columnconfigure(1, weight=1)

        # --- Layout usando Pack para os botões DENTRO de frame_botoes ---
        self.btn_login.pack(side=tk.LEFT, padx=5)
        self.btn_cadastrar.pack(side=tk.LEFT, padx=5)
        
        # Foco inicial
        self.ent_email.focus()

        # Permitir que Enter no campo de senha acione o login
        self.ent_senha.bind("<Return>", lambda event: self._realizar_login())
        self.ent_email.bind("<Return>", lambda event: self.ent_senha.focus())


    def _realizar_login(self):
        """
        Coleta email e senha e tenta realizar o login através do app_controller.
        """
        email = self.ent_email.get()
        senha = self.ent_senha.get()

        if not email or not senha:
            messagebox.showwarning("Login Inválido", "Por favor, preencha email e senha.")
            return

        self.app_controller.realizar_login(email, senha)

    def _abrir_cadastro(self):
        """
        Placeholder para a funcionalidade de abrir a tela de cadastro.
        """
        self.app_controller.mostrar_tela_cadastro()


    def limpar_campos(self):
        """Limpa os campos de email e senha."""
        self.ent_email.delete(0, tk.END)
        self.ent_senha.delete(0, tk.END)
        self.ent_email.focus()

# Exemplo de como usar esta tela (para teste, seria chamado pelo main.py ou um controlador)
if __name__ == '__main__':
    # Mock do AppController para teste
    class MockAppController:
        def __init__(self, root_window):
            self.root = root_window
            self.gerenciador_dados = None 

        def realizar_login(self, email, senha):
            print(f"Tentativa de login com Email: {email}, Senha: {senha}")
            if email == "teste@teste.com" and senha == "123":
                messagebox.showinfo("Login Bem-sucedido", f"Bem-vindo, {email}!")
            else:
                messagebox.showerror("Falha no Login", "Email ou senha incorretos.")
        
        def mostrar_tela_cadastro(self):
            messagebox.showinfo("Navegação", "Indo para a tela de cadastro (simulado).")


    root = tk.Tk()
    root.title("Sistema de Gestão Educacional - Login")
    root.geometry("450x250") 

    window_width = 450
    window_height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False) 

    mock_controller = MockAppController(root)
    login_view = TelaLogin(root, mock_controller)
    
    root.mainloop()
