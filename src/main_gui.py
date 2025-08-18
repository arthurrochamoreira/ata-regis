"""Application entry point configuring page and wiring MVC components."""

from __future__ import annotations

import flet as ft

from services.ata_service import AtaService
from controllers.dashboard_controller import DashboardController
from ui.main_view import MainView
from theme.tokens import TOKENS as T
from theme import colors as C


def main(page: ft.Page) -> None:
    """Bootstraps Flet page and attaches controller/view."""
    page.title = "Gestor ARP"
    page.padding = 0
    page.bgcolor = C.BG_APP
    page.fonts = {T.typography.FONT_SANS: "https://fonts.gstatic.com/s/inter/v7/Inter-Regular.ttf"}
    page.theme = ft.Theme(color_scheme_seed="blue", font_family=T.typography.FONT_SANS)

    view = MainView(controller=None)
    controller = DashboardController(view=view, ata_service=AtaService())
    view._c = controller
    page.add(view)


if __name__ == "__main__":
    ft.app(target=main)
