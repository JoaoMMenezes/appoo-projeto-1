# interface/tela_menu.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any 

class TelaMenuBase(ttk.Frame):
    def __init__(self, container: tk.Tk | ttk.Frame, app_controller, usuario_logado: Any):
        super().__init__(container)
        self.container = container
        self.app_controller = app_controller
        self.usuario_logado = usuario_logado
        self.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self._configurar_interface_comum()
        self._configurar_interface_especifica()

    def _configurar_interface_comum(self):
        self.lbl_boas_vindas = ttk.Label(
            self, 
            text=f"Bem-vindo(a), {self.usuario_logado.nome} ({self.usuario_logado.obter_tipo_usuario()})!",
            font=('Helvetica', 14, 'bold')
        )
        self.lbl_boas_vindas.pack(pady=10)
        self.btn_logout = ttk.Button(self, text="Logout", command=self._fazer_logout)
        self.btn_logout.pack(pady=10, side=tk.BOTTOM)

    def _configurar_interface_especifica(self): pass 

    def _fazer_logout(self):
        if messagebox.askyesno("Logout", "Tem certeza que deseja sair?"):
            self.app_controller.realizar_logout()

class TelaMenuAluno(TelaMenuBase):
    def _configurar_interface_especifica(self):
        super()._configurar_interface_especifica()
        lbl_titulo_aluno = ttk.Label(self, text="Dashboard do Aluno", font=('Helvetica', 12, 'italic'))
        lbl_titulo_aluno.pack(pady=5)
        frame_acoes = ttk.Frame(self)
        frame_acoes.pack(pady=10, padx=10, fill="x", expand=True)

        btn_listar_cursos = ttk.Button(frame_acoes, text="Listar Cursos Disponíveis", command=self.listar_cursos)
        btn_listar_cursos.pack(fill="x", pady=3)

        btn_inscrever_turma = ttk.Button(frame_acoes, text="Inscrever-se em Turma", command=self.inscrever_turma) # << MODIFICADO
        btn_inscrever_turma.pack(fill="x", pady=3)

        btn_acessar_trilha = ttk.Button(frame_acoes, text="Acessar Trilha de Aprendizagem", command=self.acessar_trilha)
        btn_acessar_trilha.pack(fill="x", pady=3)

        btn_ver_avaliacoes = ttk.Button(frame_acoes, text="Visualizar Minhas Avaliações", command=self.ver_avaliacoes)
        btn_ver_avaliacoes.pack(fill="x", pady=3)

    def listar_cursos(self):
        self.app_controller.mostrar_tela_listagem_cursos_aluno()

    def inscrever_turma(self): # << MODIFICADO
        self.app_controller.mostrar_tela_inscricao_turma_aluno()

    def acessar_trilha(self): # << MODIFICADO
        # Anteriormente chamava: self.app_controller.mostrar_tela_placeholder("Acessar Trilha de Aprendizagem")
        self.app_controller.mostrar_tela_visualizar_trilhas_aluno()
        
    def ver_avaliacoes(self): # << MODIFICADO
        # Anteriormente chamava: self.app_controller.mostrar_tela_placeholder("Visualizar Minhas Avaliações")
        self.app_controller.mostrar_tela_visualizar_notas_aluno()
    # ...


class TelaMenuProfessor(TelaMenuBase):
    def _configurar_interface_especifica(self):
        super()._configurar_interface_especifica()
        lbl_titulo_prof = ttk.Label(self, text="Dashboard do Professor", font=('Helvetica', 12, 'italic'))
        lbl_titulo_prof.pack(pady=5)
        frame_acoes = ttk.Frame(self)
        frame_acoes.pack(pady=10, padx=10, fill="x", expand=True)
        btn_gerenciar_cursos = ttk.Button(frame_acoes, text="Gerenciar Cursos", command=self.gerenciar_cursos)
        btn_gerenciar_cursos.pack(fill="x", pady=3)
        btn_gerenciar_turmas = ttk.Button(frame_acoes, text="Gerenciar Turmas", command=self.gerenciar_turmas)
        btn_gerenciar_turmas.pack(fill="x", pady=3)
        btn_publicar_aulas = ttk.Button(frame_acoes, text="Publicar Aulas/Atividades", command=self.publicar_conteudo)
        btn_publicar_aulas.pack(fill="x", pady=3)
        btn_lancar_notas = ttk.Button(frame_acoes, text="Lançar/Ver Notas", command=self.lancar_ver_notas)
        btn_lancar_notas.pack(fill="x", pady=3)

    def gerenciar_cursos(self): self.app_controller.mostrar_tela_gerenciamento_cursos_professor()
    def gerenciar_turmas(self): self.app_controller.mostrar_tela_gerenciamento_turmas()
    # def publicar_conteudo(self): self.app_controller.mostrar_tela_editar_trilha()
    def publicar_conteudo(self): self.app_controller.mostrar_tela_gerenciar_atividades_turma()

    def lancar_ver_notas(self): self.app_controller.mostrar_tela_lancar_notas()

class TelaMenuCoordenador(TelaMenuBase):
    def _configurar_interface_especifica(self):
        super()._configurar_interface_especifica()
        lbl_titulo_coord = ttk.Label(self, text="Dashboard do Coordenador", font=('Helvetica', 12, 'italic'))
        lbl_titulo_coord.pack(pady=5)
        frame_acoes = ttk.Frame(self)
        frame_acoes.pack(pady=10, padx=10, fill="x", expand=True)
        btn_gerenciar_usuarios = ttk.Button(frame_acoes, text="Gerenciar Usuários", command=self.gerenciar_usuarios)
        btn_gerenciar_usuarios.pack(fill="x", pady=3)
        btn_gerenciar_cursos_coord = ttk.Button(frame_acoes, text="Gerenciar Cursos", command=self.gerenciar_cursos_coord)
        btn_gerenciar_cursos_coord.pack(fill="x", pady=3)
        btn_gerenciar_turmas_coord = ttk.Button(frame_acoes, text="Gerenciar Turmas", command=self.gerenciar_turmas_coord) 
        btn_gerenciar_turmas_coord.pack(fill="x", pady=3)
        btn_relatorios = ttk.Button(frame_acoes, text="Relatórios de Desempenho", command=self.ver_relatorios)
        btn_relatorios.pack(fill="x", pady=3)
        btn_config_trilhas = ttk.Button(frame_acoes, text="Configurar Trilhas de Aprendizagem", command=self.configurar_trilhas)
        btn_config_trilhas.pack(fill="x", pady=3)
        btn_auditar_conteudo = ttk.Button(frame_acoes, text="Auditar Conteúdo", command=self.auditar_conteudo)
        btn_auditar_conteudo.pack(fill="x", pady=3)

    def gerenciar_usuarios(self): self.app_controller.mostrar_tela_gerenciar_usuarios()
    def gerenciar_cursos_coord(self): self.app_controller.mostrar_tela_gerenciamento_cursos_professor()
    def gerenciar_turmas_coord(self): self.app_controller.mostrar_tela_gerenciamento_turmas()
    def ver_relatorios(self): messagebox.showinfo("Coordenador", "Funcionalidade: Relatórios de Desempenho (Não implementado)")
    def configurar_trilhas(self): self.app_controller.mostrar_tela_editar_trilha()
    def auditar_conteudo(self): messagebox.showinfo("Coordenador", "Funcionalidade: Auditar Conteúdo (Não implementado)") # Pode chamar mostrar_tela_placeholder

# Exemplo de como usar estas telas (para teste)
if __name__ == '__main__':
    class MockAppController:
        def __init__(self, root_window): self.root = root_window
        def realizar_logout(self):
            messagebox.showinfo("Logout", "Usuário deslogado!")
            for widget in self.root.winfo_children(): widget.destroy()
            ttk.Label(self.root, text="Tela de Login Simulada").pack(padx=20, pady=20)
        def mostrar_tela_listagem_cursos_aluno(self): messagebox.showinfo("Navegação", "Listando Cursos (Aluno).")
        def mostrar_tela_inscricao_turma_aluno(self): messagebox.showinfo("Navegação", "Inscrevendo em Turma (Aluno).")
        def mostrar_tela_placeholder(self, funcionalidade): messagebox.showinfo("Em Desenvolvimento", f"A funcionalidade '{funcionalidade}' ainda não foi implementada.")
        def mostrar_tela_gerenciamento_cursos_professor(self): messagebox.showinfo("Navegação", "Gerenciando Cursos.")
        def mostrar_tela_gerenciamento_turmas(self): messagebox.showinfo("Navegação", "Gerenciando Turmas.")
    class MockUsuario:
        def __init__(self, nome, tipo): self.nome = nome; self.tipo_usuario = tipo
        def obter_tipo_usuario(self): return self.tipo_usuario

    root = tk.Tk(); root.title("Sistema de Gestão Educacional - Menu"); root.geometry("500x480")
    mock_controller = MockAppController(root)
    usuario_aluno = MockUsuario("Zeca Aluno", "Aluno") # Teste Aluno
    menu_aluno = TelaMenuAluno(root, mock_controller, usuario_aluno)
    root.mainloop()
