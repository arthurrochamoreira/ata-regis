"""Status badge component."""

from __future__ import annotations

from typing import Literal

import flet as ft

from theme.tokens import TOKENS as T

C, S, R, SH, M, TY = (
    T.colors,
    T.spacing,
    T.radius,
    T.shadows,
    T.motion,
    T.typography,
)

_VARIANTS: dict[str, tuple[str, str]] = {
    "success": (C.SUCCESS_TEXT, C.SUCCESS_BG),
    "warning": (C.WARNING_TEXT, C.WARNING_BG),
    "error": (C.ERROR_TEXT, C.ERROR_BG),
}


def StatusBadge(variant: Literal["success", "warning", "error"], text: str) -> ft.Container:
    """Badge with colored dot indicating status."""

    fg, bg = _VARIANTS[variant]
    dot = ft.Container(
        width=S.SPACE_2,
        height=S.SPACE_2,
        bgcolor=fg,
        border_radius=R.RADIUS_FULL,
    )
    label = ft.Text(
        text,
        size=TY.SMALL["size"],
        color=fg,
        weight=ft.FontWeight.W_500,
    )
    content = ft.Row([dot, label], spacing=S.SPACE_2, alignment=ft.MainAxisAlignment.CENTER)
    return ft.Container(
        content=content,
        bgcolor=bg,
        padding=ft.padding.symmetric(horizontal=S.SPACE_2, vertical=S.SPACE_1),
        border_radius=R.RADIUS_FULL,
    )


# Example usage:
# badge = StatusBadge("success", "Ativo")
