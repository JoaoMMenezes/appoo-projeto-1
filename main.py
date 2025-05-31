# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import uuid 
from typing import List, Optional, Tuple, Dict 

from persistencia.gerenciador_dados import GerenciadorDados
from usuarios.usuario import Usuario 
from usuarios.aluno import Aluno
from usuarios.professor import Professor
from usuarios.coordenador import Coordenador
from entidades.curso import Curso
from entidades.turma import Turma 
from entidades.atividade import Atividade

from interface.tela_login import TelaLogin
from interface.tela_menu import TelaMenuAluno, TelaMenuProfessor, TelaMenuCoordenador
from interface.tela_gerenciar_cursos import TelaGerenciarCursos 
from interface.tela_listar_cursos_aluno import TelaListarCursosAluno
from interface.tela_gerenciar_turmas import TelaGerenciarTurmas
from interface.tela_listar_inscrever_turmas_aluno import TelaListarInscreverTurmasAluno
from interface.tela_gerenciar_atividades_turma import TelaGerenciarAtividadesTurma

from entidades.trilha import TrilhaAprendizagem
from entidades.avaliacao import Avaliacao
from interface.tela_visualizar_trilhas_aluno import TelaVisualizarTrilhasAluno
from interface.tela_visualizar_notas_aluno import TelaVisualizarNotasAluno

class AppController:
    ARQUIVO_ALUNOS = 'alunos.json'
    ARQUIVO_PROFESSORES = 'professores.json'
    ARQUIVO_COORDENADORES = 'coordenadores.json'
    ARQUIVO_CURSOS = 'cursos.json'
    ARQUIVO_TURMAS = 'turmas.json'
    ARQUIVO_ATIVIDADES = 'atividades.json'
    ARQUIVO_AVALIACOES = 'avaliacoes.json' 
    ARQUIVO_TRILHAS = 'trilhas.json'
# Continuacao da classe AppController:
    def __init__(self, root_window: tk.Tk):
        self.root = root_window
        self.root.title("Sistema de Gestão Educacional")
        self.root.geometry("600x400") 

        self.centralizar_janela(600, 400)
        
        self.gerenciador_dados = GerenciadorDados()
        self.usuario_logado: Usuario | None = None 

        self.alunos: List[Aluno] = []
        self.professores: List[Professor] = []
        self.coordenadores: List[Coordenador] = []
        self.cursos: List[Curso] = []
        self.turmas: List[Turma] = []
        self.atividades: List[Atividade] = []
        self.avaliacoes: List[Avaliacao] = [] # Para o futuro
        self.trilhas: List[TrilhaAprendizagem] = [] # Para o futuro

        self._carregar_todos_os_dados()

        self.current_frame: ttk.Frame | None = None
        self.current_toplevel: tk.Toplevel | None = None 
        self.mostrar_tela_login()

    def centralizar_janela(self, width: int, height: int, toplevel_window: Optional[tk.Toplevel] = None):
        # Garante que a janela (root ou toplevel) seja centralizada na tela.
        window = toplevel_window if toplevel_window else self.root
        window.update_idletasks() # Atualiza as dimensões da janela antes de calcular a posição
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Usa as dimensões desejadas para Toplevels, ou as atuais para a root
        if toplevel_window:
            actual_width = width
            actual_height = height
        else: 
            actual_width = window.winfo_width()
            actual_height = window.winfo_height()
            # Fallback para dimensões desejadas se as atuais forem muito pequenas (primeira vez)
            if actual_width < 50: actual_width = width
            if actual_height < 50: actual_height = height

        x = (screen_width // 2) - (actual_width // 2)
        y = (screen_height // 2) - (actual_height // 2)
        window.geometry(f'{actual_width}x{actual_height}+{x}+{y}')

    def _carregar_todos_os_dados(self):
        # Carrega todos os dados dos arquivos JSON para listas na memória.
        dados_alunos = self.gerenciador_dados.carregar_dados(self.ARQUIVO_ALUNOS)
        self.alunos = [Aluno.from_dict(data) for data in dados_alunos if isinstance(data, dict)]
        
        dados_professores = self.gerenciador_dados.carregar_dados(self.ARQUIVO_PROFESSORES)
        self.professores = [Professor.from_dict(data) for data in dados_professores if isinstance(data, dict)]

        dados_coordenadores = self.gerenciador_dados.carregar_dados(self.ARQUIVO_COORDENADORES)
        self.coordenadores = [Coordenador.from_dict(data) for data in dados_coordenadores if isinstance(data, dict)]
        
        dados_cursos = self.gerenciador_dados.carregar_dados(self.ARQUIVO_CURSOS)
        self.cursos = [Curso.from_dict(data) for data in dados_cursos if isinstance(data, dict)]

        dados_turmas = self.gerenciador_dados.carregar_dados(self.ARQUIVO_TURMAS)
        self.turmas = [Turma.from_dict(data) for data in dados_turmas if isinstance(data, dict)]
        
        dados_atividades = self.gerenciador_dados.carregar_dados(self.ARQUIVO_ATIVIDADES)
        self.atividades = [Atividade.from_dict(data) for data in dados_atividades if isinstance(data, dict)]

       # Carregar avaliações
        dados_avaliacoes = self.gerenciador_dados.carregar_dados(self.ARQUIVO_AVALIACOES)
        self.avaliacoes = [Avaliacao.from_dict(data) for data in dados_avaliacoes if isinstance(data, dict)]

        # Carregar trilhas
        dados_trilhas = self.gerenciador_dados.carregar_dados(self.ARQUIVO_TRILHAS)
        self.trilhas = [TrilhaAprendizagem.from_dict(data) for data in dados_trilhas if isinstance(data, dict)]
      
        print("Dados carregados:")
        print(f"  {len(self.alunos)} alunos")
        print(f"  {len(self.professores)} professores")
        print(f"  {len(self.coordenadores)} coordenadores")
        print(f"  {len(self.cursos)} cursos")
        print(f"  {len(self.turmas)} turmas")
        print(f"  {len(self.atividades)} atividades")
        print(f"  {len(self.avaliacoes)} avaliações, {len(self.trilhas)} trilhas") # 
        self._criar_dados_iniciais_se_necessario()

    def _criar_dados_iniciais_se_necessario(self):
        # Cria dados de exemplo (usuários, cursos, turmas, atividades) se os arquivos JSON estiverem vazios.
        algo_foi_criado = False

        if not self.alunos and not self.professores and not self.coordenadores:
            print("Nenhum usuário encontrado. Criando dados iniciais de usuários...")
            coord1 = Coordenador(str(uuid.uuid4()), "Admin Coordenador", "coord@sistema.com", "admin123", "Geral")
            self.coordenadores.append(coord1)
            prof1 = Professor(str(uuid.uuid4()), "Prof. Xavier", "prof@sistema.com", "prof123", "Exatas")
            self.professores.append(prof1)
            aluno1 = Aluno(str(uuid.uuid4()), "Aluno Teste", "aluno@sistema.com", "aluno123", "MAT001")
            self.alunos.append(aluno1)
            algo_foi_criado = True
            print("Dados iniciais de usuários criados.")

        if not self.cursos:
            print("Nenhum curso encontrado. Criando cursos de exemplo...")
            curso_exemplo = Curso(id_curso=str(uuid.uuid4()), nome_curso="Introdução à Programação",
                                  descricao="Conceitos básicos de lógica e Python.", carga_horaria=40)
            self.cursos.append(curso_exemplo)
            curso_web = Curso(id_curso=str(uuid.uuid4()), nome_curso="Desenvolvimento Web Básico",
                              descricao="HTML, CSS e JavaScript.", carga_horaria=60)
            self.cursos.append(curso_web)
            algo_foi_criado = True
            print("Cursos de exemplo criados.")

        if not self.turmas and self.cursos and self.professores:
            print("Nenhuma turma encontrada. Criando turmas de exemplo...")
            if len(self.cursos) > 0 and len(self.professores) > 0:
                turma_ex1 = Turma(id_turma=str(uuid.uuid4()), id_curso=self.cursos[0].id_curso, nome_turma="PROG-M1", max_alunos=3, id_professor=self.professores[0].id_usuario)
                self.turmas.append(turma_ex1)
                self.cursos[0].adicionar_turma(turma_ex1.id_turma) 
                self.professores[0].adicionar_turma(turma_ex1.id_turma) 
                algo_foi_criado = True

            if len(self.cursos) > 1: 
                turma_ex2 = Turma(id_turma=str(uuid.uuid4()), id_curso=self.cursos[1].id_curso, nome_turma="WEB-T1", max_alunos=20)
                self.turmas.append(turma_ex2)
                self.cursos[1].adicionar_turma(turma_ex2.id_turma)
                algo_foi_criado = True
            print("Turmas de exemplo criadas.")
        
        if not self.atividades and self.turmas:
            print("Nenhuma atividade encontrada. Criando atividades de exemplo...")
            if len(self.turmas) > 0:
                id_turma_exemplo = self.turmas[0].id_turma
                ativ1 = Atividade(str(uuid.uuid4()), id_turma_exemplo, "Primeiro Trabalho de Python", "Resolver os exercícios do Cap. 1", "15/06/2025", "Trabalho")
                self.atividades.append(ativ1)
                turma_obj = self.obter_turma_por_id(id_turma_exemplo)
                if turma_obj:
                    turma_obj.adicionar_atividade(ativ1.id_atividade)
                
                ativ2 = Atividade(str(uuid.uuid4()), self.turmas[0].id_turma, "Prova Parcial 1", "Conteúdo das primeiras 5 aulas.", "30/06/2025", "Prova")
                self.atividades.append(ativ2)
                if turma_obj:
                    turma_obj.adicionar_atividade(ativ2.id_atividade)
                algo_foi_criado = True
            print("Atividades de exemplo criadas.")

        if not self.trilhas and (self.cursos or self.atividades):
            print("Nenhuma trilha encontrada. Criando trilha de exemplo...")
            trilha1 = TrilhaAprendizagem(str(uuid.uuid4()), "Fundamentos de Python", 
                                        "Aprenda o básico da programação com Python.",
                                        publico_alvo="Iniciantes")
            if self.cursos: # Adiciona o primeiro curso como item
                trilha1.adicionar_item("curso", self.cursos[0].id_curso, self.cursos[0].nome_curso)
            if self.atividades: # Adiciona a primeira atividade
                trilha1.adicionar_item("atividade", self.atividades[0].id_atividade, self.atividades[0].titulo)
            self.trilhas.append(trilha1)
            algo_foi_criado = True # Certifique-se que esta variável é usada para decidir se salva
            print("Trilha de exemplo criada.")

        # Criar avaliações de exemplo se houver alunos, atividades, turmas e professores
        if not self.avaliacoes and self.alunos and self.atividades and self.turmas and self.professores:
            print("Nenhuma avaliação encontrada. Criando avaliação de exemplo...")
            aluno_ex = self.alunos[0]
            prof_ex = self.professores[0]
            # Tenta encontrar uma atividade ligada a uma turma para criar uma avaliação de exemplo
            for turma_ex in self.turmas:
                # Verifica se o aluno está na turma ou se a turma está vazia (apenas para exemplo)
                # Idealmente, o aluno deveria estar na turma.
                aluno_na_turma = aluno_ex.id_usuario in turma_ex.lista_id_alunos
                if aluno_na_turma or not turma_ex.lista_id_alunos : 
                    atividades_da_turma = [a for a in self.atividades if a.id_turma_ou_curso == turma_ex.id_turma]
                    if atividades_da_turma:
                        ativ_ex = atividades_da_turma[0]
                        aval1 = Avaliacao(str(uuid.uuid4()), aluno_ex.id_usuario, ativ_ex.id_atividade, turma_ex.id_turma,
                                          nota="8.5", feedback_professor="Muito bom esforço!", 
                                          id_professor_avaliador=prof_ex.id_usuario)
                        self.avaliacoes.append(aval1)
                        algo_foi_criado = True # Certifique-se que esta variável é usada
                        print("Avaliação de exemplo criada.")
                        break # Cria apenas uma avaliação de exemplo para simplificar
            
        if algo_foi_criado: # Esta condição já deve existir no seu método
            self.salvar_todos_os_dados()

    def salvar_todos_os_dados(self):
        # Salva o estado atual das listas de entidades nos respectivos arquivos JSON.
        self.gerenciador_dados.salvar_dados(self.ARQUIVO_ALUNOS, [a.to_dict() for a in self.alunos])
        self.gerenciador_dados.salvar_dados(self.ARQUIVO_PROFESSORES, [p.to_dict() for p in self.professores])
        self.gerenciador_dados.salvar_dados(self.ARQUIVO_COORDENADORES, [c.to_dict() for c in self.coordenadores])
        self.gerenciador_dados.salvar_dados(self.ARQUIVO_CURSOS, [c.to_dict() for c in self.cursos])
        self.gerenciador_dados.salvar_dados(self.ARQUIVO_TURMAS, [t.to_dict() for t in self.turmas])
        self.gerenciador_dados.salvar_dados(self.ARQUIVO_ATIVIDADES, [at.to_dict() for at in self.atividades])
        # ... (após salvar self.atividades) ...
        self.gerenciador_dados.salvar_dados(self.ARQUIVO_AVALIACOES, [av.to_dict() for av in self.avaliacoes])
        self.gerenciador_dados.salvar_dados(self.ARQUIVO_TRILHAS, [tr.to_dict() for tr in self.trilhas])
        # ... (o print "Todos os dados foram salvos." já deve estar no final)
        print("Todos os dados foram salvos.")
# Continuacao da classe AppController:
    def _limpar_frame_atual(self):
        # Remove o frame principal atual e fecha qualquer Toplevel aberta.
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
        if self.current_toplevel: 
            try:
                self.current_toplevel.destroy()
            except tk.TclError: # Janela pode já ter sido fechada pelo utilizador
                pass
            self.current_toplevel = None

    def mostrar_tela_login(self):
        # Configura e exibe a tela de login.
        self._limpar_frame_atual()
        self.usuario_logado = None 
        self.root.title("Login - Sistema Educacional")
        self.root.geometry("450x250") 
        self.centralizar_janela(450,250)
        self.root.resizable(False, False) # Impede redimensionamento da tela de login
        self.current_frame = TelaLogin(self.root, self)
        if isinstance(self.current_frame, TelaLogin): 
             self.current_frame.limpar_campos()

    def realizar_login(self, email: str, senha_fornecida: str):
        # Valida as credenciais e direciona para o dashboard apropriado.
        todos_usuarios = self.alunos + self.professores + self.coordenadores
        usuario_encontrado: Usuario | None = None
        for usr in todos_usuarios:
            if usr.email == email:
                usuario_encontrado = usr
                break
        
        if usuario_encontrado and usuario_encontrado.verificar_senha(senha_fornecida):
            self.usuario_logado = usuario_encontrado
            messagebox.showinfo("Login Bem-sucedido", f"Bem-vindo(a), {self.usuario_logado.nome}!")
            self._abrir_dashboard_usuario()
        else:
            messagebox.showerror("Falha no Login", "Email ou senha incorretos.")
            if isinstance(self.current_frame, TelaLogin): 
                self.current_frame.limpar_campos()

    def _abrir_dashboard_usuario(self):
        # Abre o dashboard específico para o tipo de utilizador logado.
        if not self.usuario_logado:
            self.mostrar_tela_login() 
            return

        self._limpar_frame_atual()
        self.root.resizable(True, True) # Permite redimensionar dashboards
        self.root.geometry("600x400") # Tamanho padrão para dashboards
        self.centralizar_janela(600,400) 
        
        tipo = self.usuario_logado.obter_tipo_usuario()
        self.root.title(f"Dashboard {tipo} - Sistema Educacional")

        if tipo == "Aluno":
            self.current_frame = TelaMenuAluno(self.root, self, self.usuario_logado)
        elif tipo == "Professor":
            self.current_frame = TelaMenuProfessor(self.root, self, self.usuario_logado)
        elif tipo == "Coordenador":
            self.current_frame = TelaMenuCoordenador(self.root, self, self.usuario_logado)
        else:
            messagebox.showerror("Erro", "Tipo de usuário desconhecido.")
            self.mostrar_tela_login()

    def realizar_logout(self):
        # Desloga o utilizador e retorna à tela de login.
        self.usuario_logado = None
        messagebox.showinfo("Logout", "Você foi desconectado.")
        self.mostrar_tela_login()

    def mostrar_tela_cadastro(self):
        # Placeholder para a funcionalidade de cadastro de novos utilizadores.
        messagebox.showinfo("Em Desenvolvimento", "A tela de cadastro de usuários ainda será implementada.")
    
    def mostrar_tela_placeholder(self, titulo_funcionalidade: str):
        # Exibe uma janela Toplevel genérica para funcionalidades em desenvolvimento.
        if self.current_toplevel and self.current_toplevel.winfo_exists():
            try:
                self.current_toplevel.destroy()
            except tk.TclError:
                pass 

        placeholder_window = tk.Toplevel(self.root)
        placeholder_window.title(titulo_funcionalidade)
        placeholder_window.geometry("400x200")
        self.centralizar_janela(400, 200, toplevel_window=placeholder_window)
        placeholder_window.transient(self.root) # Define como janela filha da root
        placeholder_window.grab_set() # Torna a janela modal

        lbl_titulo = ttk.Label(placeholder_window, text=titulo_funcionalidade, font=('Helvetica', 16, 'bold'))
        lbl_titulo.pack(pady=20)
        
        lbl_mensagem = ttk.Label(placeholder_window, text="Esta funcionalidade ainda está em desenvolvimento.\nVolte em breve!", justify="center")
        lbl_mensagem.pack(pady=10, padx=10)

        btn_fechar = ttk.Button(placeholder_window, text="Fechar", command=placeholder_window.destroy)
        btn_fechar.pack(pady=15)
        
        self.current_toplevel = placeholder_window # Guarda referência para gestão
# Continuacao da classe AppController:
    # --- CRUD Cursos ---
    def mostrar_tela_gerenciamento_cursos_professor(self):
        # Exibe a tela de gerenciamento de cursos.
        if self.current_toplevel and self.current_toplevel.winfo_exists(): self.current_toplevel.destroy()
        self.current_toplevel = TelaGerenciarCursos(self.root, self)
        self.centralizar_janela(800, 600, toplevel_window=self.current_toplevel)

    def obter_cursos(self) -> List[Curso]: 
        # Retorna a lista de todos os cursos.
        return self.cursos

    def obter_curso_por_id(self, id_curso: str) -> Optional[Curso]:
        # Retorna um curso específico pelo seu ID.
        return next((c for c in self.cursos if c.id_curso == id_curso), None)

    def criar_curso(self, nome: str, descricao: str, carga_horaria: int, id_curso_manual: Optional[str] = None) -> Tuple[bool, str]:
        # Cria um novo curso.
        if not nome or not descricao or carga_horaria <= 0: return False, "Nome, descrição e carga horária positiva são obrigatórios."
        id_final = id_curso_manual if id_curso_manual else str(uuid.uuid4())
        if any(c.id_curso == id_final for c in self.cursos): return False, f"Erro: ID de curso '{id_final}' já existe."
        novo_curso = Curso(id_curso=id_final, nome_curso=nome, descricao=descricao, carga_horaria=carga_horaria)
        self.cursos.append(novo_curso); self.salvar_todos_os_dados()
        return True, f"Curso '{nome}' criado com sucesso com ID: {id_final}."

    def atualizar_curso(self, id_curso: str, nome: str, descricao: str, carga_horaria: int) -> Tuple[bool, str]:
        # Atualiza os dados de um curso existente.
        curso = self.obter_curso_por_id(id_curso)
        if not curso: return False, "Curso não encontrado."
        if not nome or not descricao or carga_horaria <= 0: return False, "Dados inválidos para atualização do curso."
        curso.nome_curso = nome; curso.descricao = descricao; curso.carga_horaria = carga_horaria
        self.salvar_todos_os_dados(); return True, f"Curso '{nome}' atualizado com sucesso."

    def excluir_curso(self, id_curso: str) -> Tuple[bool, str]:
        # Exclui um curso, verificando se não está associado a turmas.
        curso = self.obter_curso_por_id(id_curso)
        if not curso: return False, "Curso não encontrado para exclusão."
        if any(t.id_curso == id_curso for t in self.turmas): return False, f"Não é possível excluir o curso '{curso.nome_curso}', pois ele está associado a uma ou mais turmas."
        self.cursos.remove(curso); self.salvar_todos_os_dados(); return True, f"Curso '{curso.nome_curso}' excluído com sucesso."
# Continuacao da classe AppController:
    # --- CRUD Turmas ---
    def mostrar_tela_gerenciamento_turmas(self):
        # Exibe a tela de gerenciamento de turmas.
        if self.current_toplevel and self.current_toplevel.winfo_exists(): self.current_toplevel.destroy()
        self.current_toplevel = TelaGerenciarTurmas(self.root, self)
        self.centralizar_janela(950, 650, toplevel_window=self.current_toplevel)

    def obter_turmas(self) -> List[Turma]: 
        # Retorna a lista de todas as turmas.
        return self.turmas

    def obter_turma_por_id(self, id_turma: str) -> Optional[Turma]:
        # Retorna uma turma específica pelo seu ID.
        return next((t for t in self.turmas if t.id_turma == id_turma), None)

    def obter_professores(self) -> List[Professor]: 
        # Retorna a lista de todos os professores (usado em ComboBoxes).
        return self.professores

    def obter_professor_por_id(self, id_professor: str) -> Optional[Professor]:
        # Retorna um professor específico pelo seu ID.
        if not id_professor: return None # Trata caso de ID None (professor não definido)
        return next((p for p in self.professores if p.id_usuario == id_professor), None)

    def criar_turma(self, id_curso: str, nome_turma: str, max_alunos: int, id_professor: Optional[str]=None, id_turma_manual: Optional[str]=None) -> Tuple[bool, str]:
        # Cria uma nova turma.
        if not id_curso or not nome_turma or max_alunos <=0: return False, "Dados obrigatórios da turma (curso, nome, máx. alunos) em falta ou inválidos."
        curso_obj = self.obter_curso_por_id(id_curso)
        if not curso_obj: return False, "Curso selecionado é inválido ou não existe."
        if id_professor and not self.obter_professor_por_id(id_professor): return False, "Professor selecionado é inválido ou não existe."
        
        id_final = id_turma_manual if id_turma_manual else str(uuid.uuid4())
        if any(t.id_turma == id_final for t in self.turmas): return False, f"Erro: ID de turma '{id_final}' já existe."
        
        nova_turma = Turma(id_final, id_curso, nome_turma, max_alunos, id_professor)
        self.turmas.append(nova_turma)
        
        curso_obj.adicionar_turma(nova_turma.id_turma) 
        if id_professor:
            prof_obj = self.obter_professor_por_id(id_professor)
            if prof_obj:
                prof_obj.adicionar_turma(nova_turma.id_turma) 
        
        self.salvar_todos_os_dados(); return True, f"Turma '{nome_turma}' criada com sucesso."

    def atualizar_turma(self, id_turma: str, id_curso: str, nome_turma: str, max_alunos: int, id_professor: Optional[str]=None) -> Tuple[bool, str]:
        # Atualiza os dados de uma turma existente.
        turma_para_atualizar = self.obter_turma_por_id(id_turma);
        if not turma_para_atualizar: return False, "Turma não encontrada para atualização."
        if not id_curso or not nome_turma or max_alunos <=0: return False, "Dados obrigatórios da turma (curso, nome, máx. alunos) em falta ou inválidos."
        
        novo_curso_obj = self.obter_curso_por_id(id_curso)
        if not novo_curso_obj: return False, "Novo curso selecionado é inválido ou não existe."
        
        novo_prof_obj = None
        if id_professor:
            novo_prof_obj = self.obter_professor_por_id(id_professor)
            if not novo_prof_obj: return False, "Novo professor selecionado é inválido ou não existe."
        
        curso_antigo_obj = self.obter_curso_por_id(turma_para_atualizar.id_curso)
        if curso_antigo_obj and turma_para_atualizar.id_curso != id_curso: 
            curso_antigo_obj.remover_turma(turma_para_atualizar.id_turma)
        
        prof_antigo_obj = self.obter_professor_por_id(turma_para_atualizar.id_professor)
        if prof_antigo_obj and turma_para_atualizar.id_professor != id_professor: 
            prof_antigo_obj.remover_turma(turma_para_atualizar.id_turma)
        
        turma_para_atualizar.id_curso=id_curso
        turma_para_atualizar.nome_turma=nome_turma
        turma_para_atualizar.max_alunos=max_alunos
        turma_para_atualizar.id_professor=id_professor
        
        novo_curso_obj.adicionar_turma(turma_para_atualizar.id_turma)
        if novo_prof_obj:
            novo_prof_obj.adicionar_turma(turma_para_atualizar.id_turma)
            
        self.salvar_todos_os_dados(); return True, f"Turma '{nome_turma}' atualizada com sucesso."

    def excluir_turma(self, id_turma: str) -> Tuple[bool, str]:
        # Exclui uma turma, verificando se não há alunos inscritos.
        turma_para_excluir = self.obter_turma_por_id(id_turma)
        if not turma_para_excluir: return False, "Turma não encontrada para exclusão."
        if turma_para_excluir.lista_id_alunos: return False, f"Não é possível excluir a turma '{turma_para_excluir.nome_turma}', pois há alunos inscritos. Remova os alunos primeiro."
        
        curso_obj = self.obter_curso_por_id(turma_para_excluir.id_curso)
        if curso_obj: curso_obj.remover_turma(turma_para_excluir.id_turma)
        
        if turma_para_excluir.id_professor:
            prof_obj = self.obter_professor_por_id(turma_para_excluir.id_professor)
            if prof_obj: prof_obj.remover_turma(turma_para_excluir.id_turma)
                
        self.turmas.remove(turma_para_excluir); self.salvar_todos_os_dados(); return True, f"Turma '{turma_para_excluir.nome_turma}' excluída com sucesso."
# Continuacao da classe AppController:
    # --- Métodos para Alunos (Inscrição, etc.) ---
    def mostrar_tela_listagem_cursos_aluno(self):
        # Exibe a tela de listagem de cursos para alunos.
        if self.current_toplevel and self.current_toplevel.winfo_exists(): self.current_toplevel.destroy()
        self.current_toplevel = TelaListarCursosAluno(self.root, self)
        self.centralizar_janela(700, 500, toplevel_window=self.current_toplevel)

    def obter_aluno_por_id(self, id_aluno: str) -> Optional[Aluno]:
        # Retorna um aluno específico pelo seu ID.
        return next((a for a in self.alunos if a.id_usuario == id_aluno), None)

    def obter_info_turmas_para_aluno(self, id_aluno_logado: str) -> List[Dict]:
        # Coleta e formata informações sobre turmas para exibição na tela de inscrição do aluno.
        aluno_logado = self.obter_aluno_por_id(id_aluno_logado)
        if not aluno_logado:
            return [] # Retorna lista vazia se o aluno não for encontrado

        lista_info_turmas = []
        for turma in self.turmas:
            curso = self.obter_curso_por_id(turma.id_curso)
            professor = self.obter_professor_por_id(turma.id_professor)
            
            vagas_disponiveis = turma.max_alunos - len(turma.lista_id_alunos)
            status_inscricao = "Disponível" # Status padrão
            if turma.id_turma in aluno_logado.turmas_inscritas:
                status_inscricao = "Já Inscrito(a)"
            elif vagas_disponiveis <= 0:
                status_inscricao = "Lotada"

            lista_info_turmas.append({
                "id_turma": turma.id_turma,
                "nome_turma": turma.nome_turma,
                "nome_curso": curso.nome_curso if curso else "Curso Não Encontrado",
                "nome_professor": professor.nome if professor else "Nenhum Professor",
                "vagas_disponiveis": vagas_disponiveis,
                "status_inscricao_aluno": status_inscricao
            })
        return lista_info_turmas

    def mostrar_tela_inscricao_turma_aluno(self):
        # Exibe a tela para o aluno se inscrever em turmas.
        if not self.usuario_logado or not isinstance(self.usuario_logado, Aluno):
            messagebox.showerror("Erro de Acesso", "Apenas alunos podem se inscrever em turmas.")
            return
            
        if self.current_toplevel and self.current_toplevel.winfo_exists():
            self.current_toplevel.destroy()
        
        self.current_toplevel = TelaListarInscreverTurmasAluno(self.root, self, self.usuario_logado.id_usuario)
        self.centralizar_janela(850, 550, toplevel_window=self.current_toplevel)
        
    def inscrever_aluno_em_turma(self, id_aluno: str, id_turma: str) -> Tuple[bool, str]:
        # Realiza a lógica de inscrição de um aluno em uma turma.
        aluno = self.obter_aluno_por_id(id_aluno)
        turma = self.obter_turma_por_id(id_turma)

        if not aluno:
            return False, "Erro: Aluno não encontrado no sistema."
        if not turma:
            return False, "Erro: Turma selecionada não encontrada no sistema."

        if id_turma in aluno.turmas_inscritas:
            return False, "Você já está inscrito(a) nesta turma."
        
        if len(turma.lista_id_alunos) >= turma.max_alunos:
            return False, "Turma lotada. Não há vagas disponíveis no momento."

        # Se todas as verificações passarem, inscreve o aluno
        aluno.inscrever_em_turma(id_turma) # Adiciona ID da turma à lista do aluno
        turma.adicionar_aluno(id_aluno)   # Adiciona ID do aluno à lista da turma
        
        self.salvar_todos_os_dados()
        return True, f"Inscrição na turma '{turma.nome_turma}' realizada com sucesso!"
# Continuacao da classe AppController:
    # --- Métodos para Gerenciamento de Atividades ---
    def mostrar_tela_gerenciar_atividades_turma(self):
        # Exibe a tela de gerenciamento de atividades para o professor logado.
        if not self.usuario_logado or not isinstance(self.usuario_logado, Professor):
            messagebox.showerror("Acesso Negado", "Apenas professores podem gerenciar atividades.")
            return

        if self.current_toplevel and self.current_toplevel.winfo_exists():
            self.current_toplevel.destroy()
        
        self.current_toplevel = TelaGerenciarAtividadesTurma(self.root, self, self.usuario_logado.id_usuario)
        self.centralizar_janela(900, 700, toplevel_window=self.current_toplevel)

    def obter_turmas_por_professor(self, id_professor: str) -> List[Turma]:
        # Retorna uma lista de turmas que um professor específico leciona.
        professor = self.obter_professor_por_id(id_professor)
        if not professor:
            return []
        
        turmas_do_professor = []
        for id_turma_lecionada in professor.turmas_lecionadas:
            turma = self.obter_turma_por_id(id_turma_lecionada)
            if turma:
                turmas_do_professor.append(turma)
        return turmas_do_professor

    def obter_atividades_por_turma(self, id_turma: str) -> List[Atividade]:
        # Retorna todas as atividades de uma turma específica.
        return [ativ for ativ in self.atividades if ativ.id_turma_ou_curso == id_turma]

    def obter_atividade_por_id(self, id_atividade: str) -> Optional[Atividade]:
        # Retorna uma atividade específica pelo ID.
        return next((ativ for ativ in self.atividades if ativ.id_atividade == id_atividade), None)

    def criar_atividade(self, id_turma: str, titulo: str, descricao: str, data_prazo: str, tipo: str, id_atividade_manual: Optional[str] = None) -> Tuple[bool, str]:
        # Cria uma nova atividade para uma turma.
        if not all([id_turma, titulo, descricao, data_prazo, tipo]):
            return False, "Todos os campos da atividade são obrigatórios."
        
        turma_obj = self.obter_turma_por_id(id_turma)
        if not turma_obj:
            return False, "Turma inválida para associar a atividade."

        id_final = id_atividade_manual if id_atividade_manual else str(uuid.uuid4())
        if any(a.id_atividade == id_final for a in self.atividades):
            return False, f"Erro: ID de atividade '{id_final}' já existe."

        nova_atividade = Atividade(id_final, id_turma, titulo, descricao, data_prazo, tipo)
        self.atividades.append(nova_atividade)
        turma_obj.adicionar_atividade(nova_atividade.id_atividade) # Associa à turma

        self.salvar_todos_os_dados()
        return True, f"Atividade '{titulo}' criada com sucesso para a turma '{turma_obj.nome_turma}'."

    def atualizar_atividade(self, id_atividade: str, id_turma: str, titulo: str, descricao: str, data_prazo: str, tipo: str) -> Tuple[bool, str]:
        # Atualiza uma atividade existente.
        atividade = self.obter_atividade_por_id(id_atividade)
        if not atividade:
            return False, "Atividade não encontrada para atualização."
        
        if not all([id_turma, titulo, descricao, data_prazo, tipo]):
            return False, "Todos os campos da atividade são obrigatórios para atualização."

        if atividade.id_turma_ou_curso != id_turma:
            turma_antiga = self.obter_turma_por_id(atividade.id_turma_ou_curso)
            if turma_antiga:
                turma_antiga.remover_atividade(id_atividade)
            
            turma_nova = self.obter_turma_por_id(id_turma)
            if turma_nova:
                turma_nova.adicionar_atividade(id_atividade)
            else: 
                return False, "Nova turma selecionada para a atividade é inválida."
            atividade.id_turma_ou_curso = id_turma

        atividade.titulo = titulo
        atividade.descricao = descricao
        atividade.data_prazo = data_prazo
        atividade.tipo = tipo
        
        self.salvar_todos_os_dados()
        return True, f"Atividade '{titulo}' atualizada com sucesso."

    def excluir_atividade(self, id_atividade: str) -> Tuple[bool, str]:
        # Exclui uma atividade.
        atividade = self.obter_atividade_por_id(id_atividade)
        if not atividade:
            return False, "Atividade não encontrada para exclusão."

        # if self.verificar_avaliacoes_para_atividade(id_atividade):
        #     return False, "Não é possível excluir a atividade, pois existem notas lançadas para ela."

        turma_associada = self.obter_turma_por_id(atividade.id_turma_ou_curso)
        if turma_associada:
            turma_associada.remover_atividade(id_atividade) 

        self.atividades.remove(atividade)
        self.salvar_todos_os_dados()
        return True, f"Atividade '{atividade.titulo}' excluída com sucesso."

    def verificar_avaliacoes_para_atividade(self, id_atividade: str) -> bool:
        # Verifica se existem avaliações (notas) lançadas para uma determinada atividade.
        # (Implementação real dependerá da entidade Avaliacao)
        print(f"INFO: Verificação de avaliações para atividade {id_atividade} não implementada completamente.")
        return False # Por enquanto, assume que não há avaliações
# Continuacao da classe AppController:
    def adicionar_aluno(self, aluno: Aluno): # Método de exemplo, pode ser expandido
        # Adiciona um novo aluno ao sistema (atualmente não usado por nenhuma tela).
        if any(a.email == aluno.email or a.matricula == aluno.matricula for a in self.alunos):
            messagebox.showerror("Erro", "Já existe um aluno com este email ou matrícula.")
            return False
        self.alunos.append(aluno)
        self.salvar_todos_os_dados()
        messagebox.showinfo("Sucesso", f"Aluno {aluno.nome} cadastrado.")
        return True
# --- Métodos para Trilhas de Aprendizagem (Visão Aluno) ---
    def obter_trilhas_disponiveis(self) -> List[TrilhaAprendizagem]:
        return self.trilhas

    def obter_trilha_por_id(self, id_trilha: str) -> Optional[TrilhaAprendizagem]:
        return next((trilha for trilha in self.trilhas if trilha.id_trilha == id_trilha), None)

    def obter_detalhes_item_trilha(self, tipo_item: str, id_item: str) -> Optional[Dict]:
        """Busca o nome/título de um curso ou atividade para exibição na trilha."""
        if tipo_item == "curso":
            curso = self.obter_curso_por_id(id_item)
            return {"nome": curso.nome_curso, "tipo": "Curso"} if curso else {"nome": "Curso não encontrado", "tipo": "Curso"}
        elif tipo_item == "atividade":
            atividade = self.obter_atividade_por_id(id_item)
            # Adicionar busca pelo nome da turma da atividade para melhor contexto
            nome_turma_contexto = ""
            if atividade:
                turma_da_atividade = self.obter_turma_por_id(atividade.id_turma_ou_curso)
                if turma_da_atividade:
                    nome_turma_contexto = f" (Turma: {turma_da_atividade.nome_turma})"
            
            return {"nome": f"{atividade.titulo}{nome_turma_contexto}", "tipo": "Atividade"} if atividade else {"nome": "Atividade não encontrada", "tipo": "Atividade"}
        return None

    def mostrar_tela_visualizar_trilhas_aluno(self):
        if not self.usuario_logado or not isinstance(self.usuario_logado, Aluno):
            messagebox.showerror("Acesso Negado", "Funcionalidade disponível apenas para alunos.")
            return
        if self.current_toplevel and self.current_toplevel.winfo_exists():
            self.current_toplevel.destroy()
        self.current_toplevel = TelaVisualizarTrilhasAluno(self.root, self, self.usuario_logado.id_usuario)
        self.centralizar_janela(800, 600, toplevel_window=self.current_toplevel)

    # --- Métodos para Avaliações (Visão Aluno) ---
    def obter_avaliacoes_formatadas_aluno(self, id_aluno: str) -> List[Dict]:
        """Retorna uma lista de dicionários com detalhes das avaliações do aluno para exibição."""
        avaliacoes_do_aluno = [av for av in self.avaliacoes if av.id_aluno == id_aluno]
        resultado_formatado = []

        for avaliacao in avaliacoes_do_aluno:
            atividade = self.obter_atividade_por_id(avaliacao.id_atividade)
            turma = self.obter_turma_por_id(avaliacao.id_turma)
            
            resultado_formatado.append({
                "id_avaliacao": avaliacao.id_avaliacao,
                "titulo_atividade": atividade.titulo if atividade else "Atividade Removida/Desconhecida",
                "nome_turma": turma.nome_turma if turma else "Turma Removida/Desconhecida",
                "nota": avaliacao.nota,
                "feedback": avaliacao.feedback_professor,
                "data_lancamento": avaliacao.data_lancamento
            })
        return resultado_formatado

    def mostrar_tela_visualizar_notas_aluno(self):
        if not self.usuario_logado or not isinstance(self.usuario_logado, Aluno):
            messagebox.showerror("Acesso Negado", "Funcionalidade disponível apenas para alunos.")
            return
        if self.current_toplevel and self.current_toplevel.winfo_exists():
            self.current_toplevel.destroy()
        self.current_toplevel = TelaVisualizarNotasAluno(self.root, self, self.usuario_logado.id_usuario)
        self.centralizar_janela(850, 500, toplevel_window=self.current_toplevel)
    def run(self):
        # Inicia o loop principal da aplicação Tkinter.
        self.root.mainloop()

# Ponto de entrada da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = AppController(root)
    app.run()
