"""Feedback components."""

from __future__ import annotations

import flet as ft
from theme.tokens import TOKENS as T
from theme import colors as C


class AlertBanner(ft.Container):
    """Simple warning banner used on dashboard."""

    def __init__(self, icon: str, title: str, subtitle: str) -> None:
        content = ft.Row(
            [
                ft.Icon(icon, color=C.WARNING_TEXT),
                ft.Column(
                    [
                        ft.Text(title, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY),
                        ft.Text(subtitle, size=T.typography.TEXT_XS, color=C.TEXT_PRIMARY),
                    ],
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=T.spacing.SPACE_3,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(
            content=content,
            bgcolor=C.WARNING_BG,
            border=ft.border.all(1, C.WARNING_TEXT),
            border_radius=T.radius.RADIUS_LG,
            padding=ft.padding.all(T.spacing.SPACE_4),
        )
        self.subtitle = content.controls[1].controls[1]  # ft.Text reference


__all__ = ["AlertBanner"]
