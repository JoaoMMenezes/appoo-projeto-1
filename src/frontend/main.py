import flet as ft

# Variáveis globais para manter o estado do usuário
usuario_logado = None
tipo_usuario = None

def main(page: ft.Page):
    page.title = "Sistema de Gerenciamento Estudantil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.window.width = 500
    page.window.height = 650
    page.window.left = 200
    page.window.top = 100
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = True

    def autenticar_usuario(e):
        global usuario_logado, tipo_usuario
        usuario = usuario_input.value
        senha = senha_input.value

        # Simulação de autenticação
        if usuario == "aluno" and senha == "123":
            usuario_logado = "aluno"
            tipo_usuario = "aluno"
            page.go("/home")
        elif usuario == "professor" and senha == "123":
            usuario_logado = "professor"
            tipo_usuario = "professor"
            page.go("/home")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Usuário ou senha incorretos!", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()

    # Elementos da tela de login
    usuario_input = ft.TextField(label="Usuário", autofocus=True)
    senha_input = ft.TextField(label="Senha", password=True, can_reveal_password=True)
    botao_login = ft.ElevatedButton(text="Entrar", on_click=autenticar_usuario)

    tela_login = ft.Column(
        [
            ft.Text("Login", size=30, weight="bold"),
            usuario_input,
            senha_input,
            botao_login,
        ],
        width=page.window.width,
        height=page.window.height - 100,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def sair():
        global usuario_logado, tipo_usuario
        usuario_logado = None
        tipo_usuario = None
        page.go("/")

    def criar_cartao(titulo: str, subtitulo: str):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(titulo, size=18, weight="bold"),
                    ft.Text(subtitulo, size=14, color=ft.Colors.GREY_700),
                ]),
                padding=15,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
            ),
            elevation=3,
            width=page.window.width - 50,
        )

    def gerar_layout_conteudo(selecao_index: int):
        conteudo = None
        titulo = ""

        if selecao_index == 0:
            titulo = "Início"
            if tipo_usuario == "aluno":
                aulas = [
                    ("Matemática", "08:00 - Sala 101"),
                    ("História", "10:00 - Sala 202"),
                    ("Física", "14:00 - Laboratório"),
                ]
            else:
                aulas = [
                    ("Biologia", "09:00 - Sala 105"),
                    ("Química", "13:00 - Sala 201"),
                ]
            conteudo = ft.Column(
                [criar_cartao(disc, horario) for disc, horario in aulas],
                scroll=ft.ScrollMode.AUTO,
                spacing=10
            )

        elif selecao_index == 1:
            titulo = "Perfil"
            conteudo = ft.Column([
                ft.Text(f"Usuário: {usuario_logado}", size=18),
                ft.Text(f"Tipo: {tipo_usuario.capitalize()}", size=18),
            ])

        elif selecao_index == 2:
            titulo = "Notas"
            if tipo_usuario == "aluno":
                notas = [("Matemática", "9.0"), ("História", "8.5"), ("Física", "10.0")]
                conteudo = ft.Column(
                    [criar_cartao(disc, f"Nota: {nota}") for disc, nota in notas],
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10
                )
            else:
                avaliacoes = [("João - Biologia", "Corrigir prova"), ("Ana - Química", "Enviar nota")]
                conteudo = ft.Column(
                    [criar_cartao(aluno, tarefa) for aluno, tarefa in avaliacoes],
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10
                )

        elif selecao_index == 3:
            titulo = "Avaliações"
            if tipo_usuario == "aluno":
                avaliacoes_futuras = [
                    ("Prova de Matemática", "25/05/2025 - 08:00"),
                    ("Trabalho de História", "28/05/2025 - 10:00"),
                    ("Exame de Física", "02/06/2025 - 14:00"),
                ]
            else:
                avaliacoes_futuras = [
                    ("Aplicar prova de Biologia", "25/05/2025 - 09:00"),
                    ("Corrigir trabalhos de Química", "29/05/2025 - 12:00"),
                ]

            conteudo = ft.Column(
                [criar_cartao(tarefa, data) for tarefa, data in avaliacoes_futuras],
                scroll=ft.ScrollMode.AUTO,
                spacing=10
            )

        return ft.Row([
            ft.NavigationRail(
                selected_index=selecao_index,
                label_type=ft.NavigationRailLabelType.ALL,
                destinations=[
                    ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Início"),
                    ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil"),
                    ft.NavigationRailDestination(icon=ft.Icons.SCHOOL, label="Notas"),
                    ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_MONTH, label="Avaliações"),
                ],
                trailing=ft.Column([
                        ft.Divider(),
                        ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Sair", on_click=lambda e: sair()),
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ), 
                on_change=lambda e: page.go(["/home", "/perfil", "/notas", "/avaliacoes"][e.control.selected_index]),
                height=page.window.height - 50,
                width= 80,
                elevation=3,
            ),
            ft.VerticalDivider(width=1),
            ft.Column([
                ft.Text(titulo, size=24, weight="bold"),
                conteudo,
            ], expand=True, spacing=20)
        ], expand=True)

    def navegar(route):
        rotas = {
            "/home": 0,
            "/perfil": 1,
            "/notas": 2,
            "/avaliacoes": 3,
        }

        if route == "/":
            page.views.clear()
            page.views.append(
                ft.View(route="/", controls=[tela_login])
            )
        elif route in rotas and usuario_logado:
            indice_pagina = rotas[route]
            page.views.clear()
            page.views.append(
                ft.View(
                    route=route,
                    controls=[gerar_layout_conteudo(indice_pagina)],
                    scroll=ft.ScrollMode.HIDDEN,
                )
            )
        else:
            page.go("/")

        page.update()

    page.on_route_change = lambda e: navegar(e.route)
    page.go("/")

ft.app(target=main)
