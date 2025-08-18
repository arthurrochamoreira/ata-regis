"""Card displaying a single metric."""

from __future__ import annotations

import flet as ft
from typing import Callable

from theme.tokens import TOKENS as T
from theme import colors as C


class MetricCard(ft.Container):
    """KPI card used in dashboard grids."""

    def __init__(
        self,
        icon: str,
        label: str,
        value: str,
        helper: str,
        on_click: Callable[[ft.ControlEvent], None] | None = None,
    ) -> None:
        self._value_ref = ft.Text(value, size=32, weight=ft.FontWeight.W_700, color=C.TEXT_PRIMARY)
        self._helper_ref = ft.Text(helper, size=T.typography.TEXT_XS, color=C.TEXT_SECONDARY)
        icon_bg = ft.colors.with_opacity(0.12, C.PRIMARY)
        header = ft.Row(
            [
                ft.Text(label, size=T.typography.TEXT_SM, weight=ft.FontWeight.W_600, color=C.TEXT_SECONDARY),
                ft.Container(
                    content=ft.Icon(icon, color=C.PRIMARY, size=T.sizes.ICON_SM),
                    width=32,
                    height=32,
                    bgcolor=icon_bg,
                    border_radius=T.radius.RADIUS_MD,
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        body = ft.Column(
            [header, self._value_ref, self._helper_ref],
            spacing=T.spacing.SPACE_2,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        super().__init__(
            content=body,
            padding=ft.padding.all(T.spacing.SPACE_5),
            bgcolor=C.SURFACE,
            border=ft.border.all(1, C.BORDER),
            border_radius=T.radius.RADIUS_LG,
            shadow=T.shadows.SHADOW_SM,
            ink=True,
            on_click=on_click,
        )

    def update_data(self, value: str, helper: str | None = None) -> None:
        """Update card numbers."""
        self._value_ref.value = value
        if helper is not None:
            self._helper_ref.value = helper
        if self.page:
            self.update()


__all__ = ["MetricCard"]
