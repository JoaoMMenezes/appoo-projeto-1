# interface/tela_gerenciar_cursos.py
import tkinter as tk
from tkinter import ttk, messagebox
import uuid # Para gerar IDs de curso

class TelaGerenciarCursos(tk.Toplevel):
    """
    Tela para professores gerenciarem cursos (criar, editar, visualizar, excluir).
    """
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller
        self.transient(master) # Mantém a janela sobre a principal
        self.grab_set() # Captura eventos, tornando a janela modal
        self.title("Gerenciar Cursos")
        self.geometry("800x600")

        # Variáveis de controle para os campos de entrada
        self.id_curso_var = tk.StringVar()
        self.nome_curso_var = tk.StringVar()
        self.descricao_var = tk.StringVar() # Usaremos Text widget para descrição, mas pode ter uma var associada
        self.carga_horaria_var = tk.StringVar()

        self._configurar_interface()
        self._carregar_cursos_existentes()

    def _configurar_interface(self):
        # --- Frame para formulário ---
        frame_formulario = ttk.LabelFrame(self, text="Detalhes do Curso", padding=(10, 10))
        frame_formulario.pack(padx=10, pady=10, fill="x", expand=False)

        # ID (geralmente não editável diretamente para novos, mas útil para visualização/edição)
        ttk.Label(frame_formulario, text="ID Curso:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_id_curso = ttk.Entry(frame_formulario, textvariable=self.id_curso_var, state="readonly", width=40)
        self.ent_id_curso.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Nome
        ttk.Label(frame_formulario, text="Nome do Curso:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_nome_curso = ttk.Entry(frame_formulario, textvariable=self.nome_curso_var, width=40)
        self.ent_nome_curso.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Descrição
        ttk.Label(frame_formulario, text="Descrição:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.txt_descricao = tk.Text(frame_formulario, height=5, width=38) # Width ajustado
        self.txt_descricao.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        # Adicionar scrollbar para descrição
        scrollbar_desc = ttk.Scrollbar(frame_formulario, orient="vertical", command=self.txt_descricao.yview)
        self.txt_descricao.configure(yscrollcommand=scrollbar_desc.set)
        scrollbar_desc.grid(row=2, column=2, sticky="ns")


        # Carga Horária
        ttk.Label(frame_formulario, text="Carga Horária (h):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ent_carga_horaria = ttk.Entry(frame_formulario, textvariable=self.carga_horaria_var, width=10)
        self.ent_carga_horaria.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        frame_formulario.columnconfigure(1, weight=1) # Faz a coluna dos inputs expandir

        # --- Frame para botões de ação ---
        frame_botoes_acao = ttk.Frame(self, padding=(10, 5))
        frame_botoes_acao.pack(fill="x", expand=False)

        self.btn_novo = ttk.Button(frame_botoes_acao, text="Novo/Limpar", command=self._limpar_formulario)
        self.btn_novo.pack(side="left", padx=5)

        self.btn_salvar = ttk.Button(frame_botoes_acao, text="Salvar Curso", command=self._salvar_curso)
        self.btn_salvar.pack(side="left", padx=5)
        
        self.btn_excluir = ttk.Button(frame_botoes_acao, text="Excluir Selecionado", command=self._excluir_curso)
        self.btn_excluir.pack(side="left", padx=5)

        # --- Frame para lista de cursos ---
        frame_lista = ttk.LabelFrame(self, text="Cursos Cadastrados", padding=(10, 10))
        frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        colunas = ("id_curso", "nome_curso", "carga_horaria")
        self.tree_cursos = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=10)
        
        self.tree_cursos.heading("id_curso", text="ID")
        self.tree_cursos.heading("nome_curso", text="Nome do Curso")
        self.tree_cursos.heading("carga_horaria", text="C.H.")

        self.tree_cursos.column("id_curso", width=250, minwidth=150, stretch=tk.NO)
        self.tree_cursos.column("nome_curso", width=300, minwidth=200)
        self.tree_cursos.column("carga_horaria", width=80, minwidth=60, stretch=tk.NO, anchor="center")

        # Scrollbar para a Treeview
        scrollbar_tree = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_cursos.yview)
        self.tree_cursos.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_cursos.pack(side="left", fill="both", expand=True)
        scrollbar_tree.pack(side="right", fill="y")

        self.tree_cursos.bind("<<TreeviewSelect>>", self._ao_selecionar_curso)

        # --- Botão Fechar ---
        btn_fechar = ttk.Button(self, text="Fechar", command=self.destroy)
        btn_fechar.pack(pady=10)
        
        self._limpar_formulario() # Inicia com formulário pronto para novo curso

    def _limpar_formulario(self):
        """Limpa os campos do formulário e prepara para um novo curso."""
        self.id_curso_var.set(str(uuid.uuid4())) # Gera novo ID para um potencial novo curso
        self.nome_curso_var.set("")
        self.txt_descricao.delete("1.0", tk.END)
        self.carga_horaria_var.set("")
        self.ent_nome_curso.focus()
        # Desselecionar qualquer item na Treeview
        if self.tree_cursos.selection():
            self.tree_cursos.selection_remove(self.tree_cursos.selection())

    def _carregar_cursos_existentes(self):
        """Carrega os cursos do controller e os exibe na Treeview."""
        # Limpa a treeview antes de carregar
        for i in self.tree_cursos.get_children():
            self.tree_cursos.delete(i)
            
        cursos = self.app_controller.obter_cursos()
        for curso in cursos:
            self.tree_cursos.insert("", tk.END, values=(curso.id_curso, curso.nome_curso, curso.carga_horaria), iid=curso.id_curso)

    def _ao_selecionar_curso(self, event=None):
        """Preenche o formulário quando um curso é selecionado na Treeview."""
        selecionado = self.tree_cursos.selection()
        if not selecionado:
            return

        id_curso_selecionado = selecionado[0] # iid é o id_curso
        curso = self.app_controller.obter_curso_por_id(id_curso_selecionado)

        if curso:
            self.id_curso_var.set(curso.id_curso)
            self.nome_curso_var.set(curso.nome_curso)
            self.txt_descricao.delete("1.0", tk.END)
            self.txt_descricao.insert("1.0", curso.descricao)
            self.carga_horaria_var.set(str(curso.carga_horaria))
        else:
            messagebox.showerror("Erro", f"Curso com ID {id_curso_selecionado} não encontrado.")
            self._limpar_formulario()


    def _salvar_curso(self):
        """Coleta dados do formulário e solicita ao controller para salvar/atualizar o curso."""
        id_curso = self.id_curso_var.get()
        nome = self.nome_curso_var.get().strip()
        descricao = self.txt_descricao.get("1.0", tk.END).strip()
        carga_horaria_str = self.carga_horaria_var.get().strip()

        if not nome or not descricao or not carga_horaria_str:
            messagebox.showerror("Erro de Validação", "Todos os campos obrigatórios (Nome, Descrição, Carga Horária) devem ser preenchidos.")
            return

        try:
            carga_horaria = int(carga_horaria_str)
            if carga_horaria <= 0:
                raise ValueError("Carga horária deve ser positiva.")
        except ValueError:
            messagebox.showerror("Erro de Validação", "Carga Horária deve ser um número inteiro positivo.")
            return

        # Verifica se é uma atualização (curso já existe na lista do Treeview)
        # ou um novo curso (ID pode ser novo ou de um curso selecionado que foi limpo)
        
        # Se o ID atual no formulário corresponde a um curso existente na lista do AppController
        curso_existente = self.app_controller.obter_curso_por_id(id_curso)

        if curso_existente: # Atualização
            sucesso, mensagem = self.app_controller.atualizar_curso(id_curso, nome, descricao, carga_horaria)
        else: # Novo curso
            # Para garantir que estamos criando com o ID no campo (que pode ter sido gerado por "Novo/Limpar")
            sucesso, mensagem = self.app_controller.criar_curso(nome, descricao, carga_horaria, id_curso_manual=id_curso)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self._carregar_cursos_existentes() # Recarrega lista
            self._limpar_formulario() # Limpa para o próximo
        else:
            messagebox.showerror("Erro", mensagem)

    def _excluir_curso(self):
        """Exclui o curso selecionado na Treeview."""
        selecionado = self.tree_cursos.selection()
        if not selecionado:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione um curso para excluir.")
            return

        id_curso_selecionado = selecionado[0]
        
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o curso ID: {id_curso_selecionado}?"):
            sucesso, mensagem = self.app_controller.excluir_curso(id_curso_selecionado)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self._carregar_cursos_existentes()
                self._limpar_formulario()
            else:
                messagebox.showerror("Erro", mensagem)

# Para testar esta tela isoladamente (opcional)
if __name__ == '__main__':
    class MockAppController:
        def __init__(self):
            self.cursos = []
            # Adicionar cursos mock para teste
            from entidades.curso import Curso # Supondo que está acessível
            self.cursos.append(Curso(str(uuid.uuid4()), "Python Básico", "Curso introdutório de Python", 40))
            self.cursos.append(Curso(str(uuid.uuid4()), "POO com Python", "Curso avançado de POO", 60))

        def obter_cursos(self):
            return self.cursos

        def obter_curso_por_id(self, id_curso):
            for c in self.cursos:
                if c.id_curso == id_curso:
                    return c
            return None

        def criar_curso(self, nome, descricao, carga_horaria, id_curso_manual=None):
            from entidades.curso import Curso
            if id_curso_manual and any(c.id_curso == id_curso_manual for c in self.cursos):
                 return False, "Erro: ID de curso já existe."
            novo_id = id_curso_manual if id_curso_manual else str(uuid.uuid4())
            novo_curso = Curso(novo_id, nome, descricao, carga_horaria)
            self.cursos.append(novo_curso)
            print(f"Curso criado: {novo_curso}")
            return True, f"Curso '{nome}' criado com sucesso!"

        def atualizar_curso(self, id_curso, nome, descricao, carga_horaria):
            curso = self.obter_curso_por_id(id_curso)
            if curso:
                curso.nome_curso = nome
                curso.descricao = descricao
                curso.carga_horaria = carga_horaria
                print(f"Curso atualizado: {curso}")
                return True, f"Curso '{nome}' atualizado com sucesso!"
            return False, "Curso não encontrado para atualização."

        def excluir_curso(self, id_curso):
            curso = self.obter_curso_por_id(id_curso)
            if curso:
                self.cursos.remove(curso)
                print(f"Curso excluído: ID {id_curso}")
                return True, f"Curso ID {id_curso} excluído com sucesso."
            return False, "Curso não encontrado para exclusão."

    root = tk.Tk()
    root.withdraw() # Esconde a janela root principal para o teste da Toplevel
    app_controller_mock = MockAppController()
    tela_gerenciar = TelaGerenciarCursos(root, app_controller_mock)
    root.mainloop()
# interface/tela_gerenciar_cursos.py