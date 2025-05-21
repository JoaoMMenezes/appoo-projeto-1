import flet as ft
from auth import autenticar

def login(page: ft.Page):
    usuario_input = ft.TextField(label="Usuário", autofocus=True)
    senha_input = ft.TextField(label="Senha", password=True, can_reveal_password=True)

    def autenticar_usuario(e):
        usuario = usuario_input.value
        senha = senha_input.value
        tipo = autenticar(usuario, senha)

        if tipo:
            page.client_storage.set("usuario_logado", usuario)
            page.client_storage.set("tipo_usuario", tipo)
            page.go("/home")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Usuário ou senha incorretos!", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    return ft.Column(
        route="/",
        controls=[
            ft.Column([
                ft.Text("Login", size=30, weight="bold"),
                usuario_input,
                senha_input,
                ft.ElevatedButton(text="Entrar", on_click=autenticar_usuario)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400)
        ]
    )