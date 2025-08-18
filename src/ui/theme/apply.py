import flet as ft

from .colors import SEM
from .typography import FONT_FAMILY


def apply_theme(page: ft.Page) -> None:
    """Apply global fonts and colors to the given page."""
    primary_font = FONT_FAMILY.split(",")[0].strip()
    page.fonts = {
        primary_font: "https://rsms.me/inter/font-files/Inter-VariableFont_slnt,wght.ttf",
    }
    page.theme = ft.Theme(font_family=primary_font)
    page.bgcolor = SEM.background
