"""Status badge component."""

from typing import Literal
import flet as ft

from theme.tokens import TOKENS as T
from theme import colors as C

S, R = T.spacing, T.radius

_VARIANTS = {
    "success": (C.SUCCESS_TEXT, C.SUCCESS_BG),
    "warning": (C.WARNING_TEXT, C.WARNING_BG),
    "error": (C.ERROR_TEXT, C.ERROR_BG),
}


def StatusBadge(label: str, variant: Literal["success", "warning", "error"] = "success") -> ft.Container:
    """Badge with colored dot indicating status."""
    dot_color, bg = _VARIANTS[variant]
    dot = ft.Container(width=8, height=8, bgcolor=dot_color, border_radius=R.RADIUS_FULL)
    content = ft.Row([dot, ft.Text(label, color=C.TEXT_PRIMARY)], spacing=S.SPACE_2)
    return ft.Container(
        content=content,
        padding=ft.padding.symmetric(vertical=S.SPACE_1, horizontal=S.SPACE_2),
        bgcolor=bg,
        border_radius=R.RADIUS_FULL,
    )
