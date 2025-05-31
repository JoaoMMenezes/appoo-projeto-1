# interface/tela_visualizar_trilhas_aluno.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from main import AppController
    from entidades.trilha import TrilhaAprendizagem

class TelaVisualizarTrilhasAluno(tk.Toplevel):
    """
    Tela para Alunos visualizarem as Trilhas de Aprendizagem disponíveis.
    """
    def __init__(self, master, app_controller: 'AppController', id_aluno_logado: str):
        super().__init__(master)
        self.app_controller = app_controller
        self.id_aluno_logado = id_aluno_logado
        
        self.transient(master)
        self.grab_set()
        self.title("Trilhas de Aprendizagem")
        self.geometry("800x600")

        self.id_trilha_selecionada = None

        self._configurar_interface()
        self._carregar_trilhas_disponiveis()

    def _configurar_interface(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para a lista de trilhas
        frame_lista_trilhas = ttk.LabelFrame(main_frame, text="Trilhas Disponíveis", padding=10)
        frame_lista_trilhas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.tree_trilhas = ttk.Treeview(frame_lista_trilhas, columns=("nome", "descricao"), show="headings", selectmode="browse")
        self.tree_trilhas.heading("nome", text="Nome da Trilha")
        self.tree_trilhas.heading("descricao", text="Descrição")
        self.tree_trilhas.column("nome", width=200)
        self.tree_trilhas.column("descricao", width=300)
        
        scrollbar_trilhas_y = ttk.Scrollbar(frame_lista_trilhas, orient=tk.VERTICAL, command=self.tree_trilhas.yview)
        self.tree_trilhas.configure(yscrollcommand=scrollbar_trilhas_y.set)
        self.tree_trilhas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_trilhas_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_trilhas.bind("<<TreeviewSelect>>", self._ao_selecionar_trilha)

        # Frame para os detalhes da trilha selecionada
        frame_detalhes_trilha = ttk.LabelFrame(main_frame, text="Itens da Trilha Selecionada", padding=10)
        frame_detalhes_trilha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.tree_itens_trilha = ttk.Treeview(frame_detalhes_trilha, columns=("ordem", "tipo", "nome"), show="headings")
        self.tree_itens_trilha.heading("ordem", text="#")
        self.tree_itens_trilha.heading("tipo", text="Tipo")
        self.tree_itens_trilha.heading("nome", text="Nome/Título do Item")
        self.tree_itens_trilha.column("ordem", width=30, anchor="center")
        self.tree_itens_trilha.column("tipo", width=80, anchor="center")
        self.tree_itens_trilha.column("nome", width=250)

        scrollbar_itens_y = ttk.Scrollbar(frame_detalhes_trilha, orient=tk.VERTICAL, command=self.tree_itens_trilha.yview)
        self.tree_itens_trilha.configure(yscrollcommand=scrollbar_itens_y.set)
        self.tree_itens_trilha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_itens_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Botão Fechar
        btn_fechar = ttk.Button(main_frame, text="Fechar", command=self.destroy)
        # Posicionar o botão de fechar abaixo dos frames, e não dentro deles.
        # Para isso, o main_frame precisaria de uma linha extra para o botão ou pack o botão depois dos frames.
        # Solução simples: pack no Toplevel
        btn_fechar_bottom = ttk.Button(self, text="Fechar", command=self.destroy)
        btn_fechar_bottom.pack(pady=10, side=tk.BOTTOM)


    def _carregar_trilhas_disponiveis(self):
        for i in self.tree_trilhas.get_children():
            self.tree_trilhas.delete(i)
        for i in self.tree_itens_trilha.get_children(): # Limpa também os itens
            self.tree_itens_trilha.delete(i)

        trilhas: List['TrilhaAprendizagem'] = self.app_controller.obter_trilhas_disponiveis()
        if not trilhas:
            self.tree_trilhas.insert("", tk.END, values=("Nenhuma trilha disponível.", ""))
        else:
            for trilha in trilhas:
                self.tree_trilhas.insert("", tk.END, values=(trilha.nome_trilha, trilha.descricao), iid=trilha.id_trilha)

    def _ao_selecionar_trilha(self, event=None):
        selecionado = self.tree_trilhas.selection()
        if not selecionado:
            return
        
        self.id_trilha_selecionada = selecionado[0] # iid é o id_trilha
        trilha_obj = self.app_controller.obter_trilha_por_id(self.id_trilha_selecionada) # Necessário no AppController

        for i in self.tree_itens_trilha.get_children():
            self.tree_itens_trilha.delete(i)

        if trilha_obj:
            for idx, item in enumerate(trilha_obj.sequencia_itens):
                tipo = item.get("tipo", "N/D").capitalize()
                id_item = item.get("id_item")
                # nome_referencia foi adicionado à entidade TrilhaAprendizagem.item
                # Se não existir, busca o nome real do curso/atividade
                nome_item = item.get("nome_referencia", "")
                if not nome_item and id_item: # Se não há nome de referência, tenta buscar
                    detalhes_item = self.app_controller.obter_detalhes_item_trilha(item.get("tipo"), id_item)
                    nome_item = detalhes_item.get("nome", "Item não encontrado") if detalhes_item else "Detalhes não disponíveis"
                
                self.tree_itens_trilha.insert("", tk.END, values=(idx + 1, tipo, nome_item))
        else:
            messagebox.showerror("Erro", "Trilha selecionada não encontrada.", parent=self)

# Teste isolado
if __name__ == '__main__':
    class MockAppController:
        def __init__(self):
            TrilhaMock = type("TrilhaMock", (), {"id_trilha":"", "nome_trilha":"", "descricao":"", "sequencia_itens":[]})
            self.trilhas = [TrilhaMock(), TrilhaMock()]
            self.trilhas[0].id_trilha="tr001"; self.trilhas[0].nome_trilha="Iniciante em Python"; self.trilhas[0].descricao="Do básico ao intermediário";
            self.trilhas[0].sequencia_itens = [
                {"tipo":"curso", "id_item":"c001", "nome_referencia":"Python Fundamentos"},
                {"tipo":"atividade", "id_item":"a001", "nome_referencia":"Exercícios de Lógica"},
                {"tipo":"curso", "id_item":"c002", "nome_referencia":"POO com Python"}
            ]
            self.trilhas[1].id_trilha="tr002"; self.trilhas[1].nome_trilha="Desenvolvimento Web Fullstack"; self.trilhas[1].descricao="Frontend e Backend";
            self.trilhas[1].sequencia_itens = [
                 {"tipo":"curso", "id_item":"c003", "nome_referencia":"HTML, CSS, JS"},
                 {"tipo":"curso", "id_item":"c004", "nome_referencia":"React Essencial"},
                 {"tipo":"curso", "id_item":"c005", "nome_referencia":"Node.js e APIs"}
            ]
        def obter_trilhas_disponiveis(self): return self.trilhas
        def obter_trilha_por_id(self, id_trilha): return next((t for t in self.trilhas if t.id_trilha == id_trilha), None)
        def obter_detalhes_item_trilha(self, tipo, id_item): # Mock
            if tipo == "curso": return {"nome": f"Curso Detalhe {id_item}"}
            if tipo == "atividade": return {"nome": f"Atividade Detalhe {id_item}"}
            return None

    root = tk.Tk()
    root.withdraw()
    mock_controller = MockAppController()
    tela_trilhas = TelaVisualizarTrilhasAluno(root, mock_controller, "aluno_teste")
    root.mainloop()
