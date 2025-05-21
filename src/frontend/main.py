import flet as ft
from routes import handle_route_change

def main(page: ft.Page):
    page.title = "Sistema de Gerenciamento Estudantil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 600
    page.window.left = 200
    page.window.top = 100
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = True
    page.window.always_on_top = True

    page.client_storage.set("usuario_logado", '')
    page.client_storage.set("tipo_usuario", '')

    page.on_route_change = lambda e: handle_route_change(e, page)
    page.go("/")

ft.app(target=main)