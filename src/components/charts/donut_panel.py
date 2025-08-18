"""Donut chart panel."""

from __future__ import annotations

from typing import Dict

import flet as ft

from theme.tokens import TOKENS as T
from theme import colors as C


class DonutPanel(ft.Container):
    """Panel displaying distribution of statuses."""

    def __init__(self, data: Dict[str, int]) -> None:
        super().__init__()
        self._data = data
        self._build()

    def _build(self) -> None:
        total = sum(self._data.values())
        colors_map = {
            "vigente": C.SUCCESS_TEXT,
            "a_vencer": C.WARNING_TEXT,
            "vencida": C.ERROR_TEXT,
        }
        sections = [
            ft.PieChartSection(value=v, color=colors_map[k], title="")
            for k, v in self._data.items()
            if v > 0
        ]
        center_r = int(240 / 2 - 16)
        pie = ft.PieChart(
            sections=sections,
            sections_space=4,
            center_space_radius=center_r,
            start_degree_offset=-90,
            expand=False,
        )
        center = ft.Column(
            [
                ft.Text(str(total), size=24, weight=ft.FontWeight.W_700, color=C.TEXT_PRIMARY),
                ft.Text("Total", size=T.typography.TEXT_XS, color=C.TEXT_SECONDARY),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        chart = ft.Container(
            width=240,
            height=240,
            alignment=ft.alignment.center,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Stack([pie, ft.Container(content=center, alignment=ft.alignment.center)]),
        )
        legend = ft.Container(
            width=240,
            content=ft.Column(
                spacing=T.spacing.SPACE_2,
                controls=[
                    self._legend_row(colors_map["vigente"], "Vigentes", self._data.get("vigente", 0), total),
                    self._legend_row(colors_map["a_vencer"], "A Vencer", self._data.get("a_vencer", 0), total),
                    self._legend_row(colors_map["vencida"], "Vencidas", self._data.get("vencida", 0), total),
                ],
            ),
        )
        self.content = ft.Column(
            [
                ft.Text("Situação das Atas", size=T.typography.TEXT_LG, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY),
                chart,
                legend,
            ],
            spacing=T.spacing.SPACE_4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.padding = ft.padding.all(T.spacing.SPACE_5)
        self.bgcolor = C.SURFACE
        self.border = ft.border.all(1, C.BORDER)
        self.border_radius = T.radius.RADIUS_LG
        self.shadow = T.shadows.SHADOW_SM

    def _legend_row(self, dot_color: str, label: str, value: int, total: int) -> ft.Row:
        pct = (value / total * 100) if total else 0
        pct_txt = f"{pct:.1f}%".replace(".", ",")
        left = ft.Row(
            spacing=T.spacing.SPACE_2,
            controls=[
                ft.Container(width=10, height=10, bgcolor=dot_color, border_radius=5),
                ft.Text(label, size=T.typography.TEXT_SM, color=C.TEXT_PRIMARY),
            ],
        )
        right = ft.Text(
            f"{value} ({pct_txt})", size=T.typography.TEXT_SM, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY
        )
        return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[left, right])

    def update_data(self, data: Dict[str, int]) -> None:
        """Replace chart data."""
        self._data = data
        self._build()
        if self.page:
            self.update()


__all__ = ["DonutPanel"]
