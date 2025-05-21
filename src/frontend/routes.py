import flet as ft
from layout import layout
from views.login import login
from views.home import home
from views.profile import profile
from views.grades import grades

# Variáveis globais (ou use page.client_storage)
usuario_logado = None
tipo_usuario = None

def handle_route_change(e: ft.RouteChangeEvent, page: ft.Page):
    global usuario_logado, tipo_usuario

    route = e.route

    # Pegue valores do client_storage para persistência entre sessões
    usuario_logado = page.client_storage.get("usuario_logado")
    tipo_usuario = page.client_storage.get("tipo_usuario")

    # Se não estiver logado e não estiver na rota login, redirecione
    if not usuario_logado and route != "/":
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[login(page)]
            )
        )
        page.update()
        return

    if route == "/":
        # Tela login (sem layout lateral)
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[login(page)]
            )
        )
    elif route == "/home":
        # Home com layout lateral
        page.views.clear()
        page.views.append(
            layout(
                page,
                home(page, tipo_usuario),
                "Início",
                0
            )
        )
    elif route == "/perfil":
        page.views.clear()
        page.views.append(
            layout(
                page,
                profile(page, usuario_logado, tipo_usuario),
                "Perfil",
                1
            )
        )
    elif route == "/notas":
        page.views.clear()
        page.views.append(
            layout(
                page,
                grades(page, tipo_usuario),
                "Notas",
                2
            )
        )
    else:
        # Rota não encontrada, volta para login
        page.go("/")

    page.update()
