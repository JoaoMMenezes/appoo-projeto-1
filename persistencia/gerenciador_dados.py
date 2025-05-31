# persistencia/gerenciador_dados.py
import json
import os

class GerenciadorDados:
    """
    Classe responsável por carregar e salvar dados em arquivos JSON.
    Garante que o diretório 'dados' exista.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Raiz do projeto appoo-projeto-1
    DATA_DIR = os.path.join(BASE_DIR, 'dados')

    def __init__(self):
        """
        Construtor da classe GerenciadorDados.
        Cria o diretório 'dados' se ele não existir.
        """
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)
            print(f"Diretório '{self.DATA_DIR}' criado.")

    def _get_caminho_arquivo(self, nome_arquivo: str) -> str:
        """
        Retorna o caminho completo para um arquivo dentro do diretório 'dados'.

        Args:
            nome_arquivo (str): O nome do arquivo JSON (ex: 'alunos.json').

        Returns:
            str: O caminho absoluto para o arquivo.
        """
        return os.path.join(self.DATA_DIR, nome_arquivo)

    def carregar_dados(self, nome_arquivo: str) -> list | dict:
        """
        Carrega dados de um arquivo JSON.

        Args:
            nome_arquivo (str): O nome do arquivo JSON a ser carregado.

        Returns:
            list | dict: Os dados carregados do arquivo. Retorna uma lista vazia
                         ou dicionário vazio se o arquivo não existir ou ocorrer um erro.
        """
        caminho = self._get_caminho_arquivo(nome_arquivo)
        try:
            if not os.path.exists(caminho):
                print(f"Aviso: Arquivo '{caminho}' não encontrado. Retornando dados vazios.")
                # Cria um arquivo vazio se não existir para evitar erros na primeira execução
                self.salvar_dados(nome_arquivo, [] if "turmas" in nome_arquivo or "alunos" in nome_arquivo or "professores" in nome_arquivo or "coordenadores" in nome_arquivo or "cursos" in nome_arquivo or "atividades" in nome_arquivo else {}) # Assume lista para entidades múltiplas
                return []
            
            with open(caminho, 'r', encoding='utf-8') as f:
                # Verifica se o arquivo está vazio
                conteudo = f.read()
                if not conteudo:
                    print(f"Aviso: Arquivo '{caminho}' está vazio. Retornando dados vazios.")
                    return [] # Ou {} dependendo da estrutura esperada
                return json.loads(conteudo)
        except json.JSONDecodeError:
            print(f"Erro: Falha ao decodificar JSON do arquivo '{caminho}'. Retornando dados vazios.")
            return [] # Ou {}
        except IOError as e:
            print(f"Erro de I/O ao carregar '{caminho}': {e}. Retornando dados vazios.")
            return [] # Ou {}

    def salvar_dados(self, nome_arquivo: str, dados: list | dict) -> bool:
        """
        Salva dados em um arquivo JSON.

        Args:
            nome_arquivo (str): O nome do arquivo JSON onde os dados serão salvos.
            dados (list | dict): Os dados a serem salvos.

        Returns:
            bool: True se os dados foram salvos com sucesso, False caso contrário.
        """
        caminho = self._get_caminho_arquivo(nome_arquivo)
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            print(f"Dados salvos com sucesso em '{caminho}'.")
            return True
        except IOError as e:
            print(f"Erro de I/O ao salvar em '{caminho}': {e}")
            return False
        except TypeError as e:
            print(f"Erro de tipo ao serializar dados para JSON em '{caminho}': {e}")
            return False

# Exemplo de uso (pode ser removido ou comentado)
if __name__ == '__main__':
    gd = GerenciadorDados()

    # Teste de salvamento e carregamento
    alunos_teste = [
        {"id": 1, "nome": "Ana Silva", "email": "ana@email.com"},
        {"id": 2, "nome": "Bruno Costa", "email": "bruno@email.com"}
    ]
    gd.salvar_dados('alunos_teste.json', alunos_teste)
    dados_carregados = gd.carregar_dados('alunos_teste.json')
    print("Alunos carregados:", dados_carregados)

    cursos_teste = [
        {"id_curso": "C001", "nome_curso": "Introdução à POO"}
    ]
    gd.salvar_dados('cursos_teste.json', cursos_teste)
    cursos_carregados = gd.carregar_dados('cursos_teste.json')
    print("Cursos carregados:", cursos_carregados)
