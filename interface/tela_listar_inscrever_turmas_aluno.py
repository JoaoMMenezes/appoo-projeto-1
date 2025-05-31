# interface/tela_listar_inscrever_turmas_aluno.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from main import AppController # Para type hinting

class TelaListarInscreverTurmasAluno(tk.Toplevel):
    """
    Tela para Alunos listarem turmas disponíveis e se inscreverem.
    """
    def __init__(self, master, app_controller: 'AppController', id_aluno_logado: str):
        super().__init__(master)
        self.app_controller = app_controller
        self.id_aluno_logado = id_aluno_logado
        
        self.transient(master)
        self.grab_set()
        self.title("Inscrever-se em Turma")
        self.geometry("850x550") # Ajustado para mais colunas

        self.id_turma_selecionada = None

        self._configurar_interface()
        self._carregar_turmas_disponiveis()

    def _configurar_interface(self):
        frame_principal = ttk.Frame(self, padding=(10, 10))
        frame_principal.pack(fill="both", expand=True)

        lbl_titulo = ttk.Label(frame_principal, text="Turmas Disponíveis para Inscrição", font=('Helvetica', 16, 'bold'))
        lbl_titulo.pack(pady=(0,10))

        # Colunas da Treeview
        colunas = ("nome_turma", "nome_curso", "professor", "vagas_disp", "status")
        self.tree_turmas = ttk.Treeview(frame_principal, columns=colunas, show="headings", height=15, selectmode="browse")
        
        self.tree_turmas.heading("nome_turma", text="Nome da Turma")
        self.tree_turmas.heading("nome_curso", text="Curso")
        self.tree_turmas.heading("professor", text="Professor")
        self.tree_turmas.heading("vagas_disp", text="Vagas Disp.")
        self.tree_turmas.heading("status", text="Status Inscrição")

        self.tree_turmas.column("nome_turma", width=150, minwidth=120)
        self.tree_turmas.column("nome_curso", width=200, minwidth=180)
        self.tree_turmas.column("professor", width=150, minwidth=120)
        self.tree_turmas.column("vagas_disp", width=100, minwidth=80, anchor="center")
        self.tree_turmas.column("status", width=150, minwidth=120, anchor="center")
        
        # Scrollbar
        scrollbar_tree = ttk.Scrollbar(frame_principal, orient="vertical", command=self.tree_turmas.yview)
        self.tree_turmas.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_turmas.pack(side="left", fill="both", expand=True)
        scrollbar_tree.pack(side="right", fill="y")

        self.tree_turmas.bind("<<TreeviewSelect>>", self._ao_selecionar_turma_treeview)

        # Frame para botões
        frame_botoes = ttk.Frame(self) # Adicionado ao Toplevel diretamente
        frame_botoes.pack(pady=10, fill="x", padx=10)

        self.btn_inscrever = ttk.Button(frame_botoes, text="Inscrever na Turma Selecionada", command=self._inscrever_aluno, state="disabled")
        self.btn_inscrever.pack(side="left", padx=(0,10))
        
        btn_atualizar = ttk.Button(frame_botoes, text="Atualizar Lista", command=self._carregar_turmas_disponiveis)
        btn_atualizar.pack(side="left", padx=(0,10))

        btn_fechar = ttk.Button(frame_botoes, text="Fechar", command=self.destroy)
        btn_fechar.pack(side="right")


    def _ao_selecionar_turma_treeview(self, event=None):
        """Habilita o botão de inscrição se uma turma elegível for selecionada."""
        selecao = self.tree_turmas.selection()
        if selecao:
            item_selecionado = self.tree_turmas.item(selecao[0])
            self.id_turma_selecionada = item_selecionado.get('tags', [None])[0] # O ID da turma estará na tag
            
            status_inscricao = item_selecionado['values'][4] # Coluna "status"

            if self.id_turma_selecionada and status_inscricao == "Disponível":
                self.btn_inscrever.config(state="normal")
            else:
                self.btn_inscrever.config(state="disabled")
                self.id_turma_selecionada = None # Limpa se não for elegível
        else:
            self.btn_inscrever.config(state="disabled")
            self.id_turma_selecionada = None

    def _carregar_turmas_disponiveis(self):
        """Carrega as turmas do controller e as exibe na Treeview."""
        # Limpa a treeview
        for i in self.tree_turmas.get_children():
            self.tree_turmas.delete(i)
        self.btn_inscrever.config(state="disabled") # Desabilita botão ao recarregar
        self.id_turma_selecionada = None

        turmas_info: List[Dict] = self.app_controller.obter_info_turmas_para_aluno(self.id_aluno_logado)
        
        if not turmas_info:
            self.tree_turmas.insert("", tk.END, values=("Nenhuma turma disponível no momento.", "", "", "", ""))
        else:
            for turma_data in turmas_info:
                # Adiciona o id_turma como uma tag para fácil recuperação
                self.tree_turmas.insert("", tk.END, 
                                        values=(turma_data["nome_turma"], 
                                                turma_data["nome_curso"], 
                                                turma_data["nome_professor"], 
                                                turma_data["vagas_disponiveis"],
                                                turma_data["status_inscricao_aluno"]),
                                        tags=(turma_data["id_turma"],))
    
    def _inscrever_aluno(self):
        if not self.id_turma_selecionada:
            messagebox.showwarning("Nenhuma Turma Selecionada", "Por favor, selecione uma turma da lista.")
            return

        confirmar = messagebox.askyesno("Confirmar Inscrição", 
                                        f"Deseja realmente se inscrever na turma selecionada?")
        if confirmar:
            sucesso, mensagem = self.app_controller.inscrever_aluno_em_turma(self.id_aluno_logado, self.id_turma_selecionada)
            if sucesso:
                messagebox.showinfo("Inscrição Realizada", mensagem)
                self._carregar_turmas_disponiveis() # Atualiza a lista para refletir a inscrição
            else:
                messagebox.showerror("Falha na Inscrição", mensagem)

# Para testar esta tela isoladamente (opcional)
if __name__ == '__main__':
    class MockAppController:
        def obter_info_turmas_para_aluno(self, id_aluno_logado):
            # Simula o retorno do AppController
            return [
                {"id_turma": "t001", "nome_turma": "PY-MANHA-2025", "nome_curso": "Python Completo", "nome_professor": "Prof. Ada", "vagas_disponiveis": 5, "status_inscricao_aluno": "Disponível"},
                {"id_turma": "t002", "nome_turma": "WEB-TARDE-2025", "nome_curso": "Web com Django", "nome_professor": "Prof. Alan", "vagas_disponiveis": 0, "status_inscricao_aluno": "Lotada"},
                {"id_turma": "t003", "nome_turma": "BD-NOITE-2025", "nome_curso": "Banco de Dados SQL", "nome_professor": "Prof. Codd", "vagas_disponiveis": 10, "status_inscricao_aluno": "Já Inscrito(a)" if id_aluno_logado == "aluno_teste_inscrito" else "Disponível"},
            ]
        
        def inscrever_aluno_em_turma(self, id_aluno, id_turma):
            if id_turma == "t001":
                print(f"Aluno {id_aluno} tentando se inscrever na turma {id_turma}")
                return True, f"Inscrição na turma {id_turma} realizada com sucesso!"
            else:
                return False, f"Não foi possível inscrever na turma {id_turma}. (Simulação)"


    root = tk.Tk()
    root.withdraw() 
    mock_controller = MockAppController()
    # Simular aluno logado
    tela_inscricao = TelaListarInscreverTurmasAluno(root, mock_controller, "aluno_teste_novo")
    # tela_inscricao = TelaListarInscreverTurmasAluno(root, mock_controller, "aluno_teste_inscrito")
    root.mainloop()
