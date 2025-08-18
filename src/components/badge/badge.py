"""Status badge component."""

from typing import Literal
import flet as ft

from theme.tokens import TOKENS as T

C, S, R = T.colors, T.spacing, T.radius

_VARIANTS = {
    "success": (C.GREEN, C.GREEN_BG),
    "warning": (C.YELLOW, C.YELLOW_BG),
    "error": (C.RED, C.RED_BG),
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
