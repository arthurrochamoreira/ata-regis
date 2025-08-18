"""Dashboard reusable components."""

from __future__ import annotations

from typing import Dict

import flet as ft
from flet import colors as fcolors

from theme.tokens import TOKENS as T
from theme import colors as C
from .badge import StatusBadge

S, R, SH, TY = T.spacing, T.radius, T.shadows, T.typography


def _hover_elevation(e: ft.HoverEvent) -> None:
    e.control.shadow = SH.SHADOW_MD if e.data == "true" else SH.SHADOW_SM
    e.control.update()


def AlertBanner(icon: str, title: str, subtitle: str) -> ft.Container:
    """Highlighted banner for important information."""
    content = ft.Row(
        [
            ft.Icon(icon, color=C.WARNING_TEXT),
            ft.Column(
                [
                    ft.Text(title, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY),
                    ft.Text(subtitle, size=TY.TEXT_XS, color=C.TEXT_PRIMARY),
                ],
                spacing=1,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=S.SPACE_3,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=content,
        bgcolor=C.WARNING_BG,
        border=ft.border.all(1, fcolors.YELLOW_200),
        border_radius=R.RADIUS_LG,
        padding=ft.padding.all(S.SPACE_4),
    )


def MetricCard(icon: str, label: str, value: str, helper: str) -> ft.Container:
    """Metric card with icon, value and helper text."""
    icon_bg = fcolors.with_opacity(0.1, C.PRIMARY)
    avatar = ft.Container(
        content=ft.Icon(icon, color=C.PRIMARY),
        width=40,
        height=40,
        bgcolor=icon_bg,
        border_radius=R.RADIUS_FULL,
        alignment=ft.alignment.center,
    )
    texts = ft.Column(
        [
            ft.Text(label.upper(), size=TY.TEXT_XS, weight=ft.FontWeight.W_600, color=C.TEXT_SECONDARY),
            ft.Text(value, size=32, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY),
            ft.Text(helper, size=TY.TEXT_XS, color=C.TEXT_SECONDARY),
        ],
        spacing=S.SPACE_1,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )
    card = ft.Container(
        content=ft.Row([avatar, texts], spacing=S.SPACE_4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.all(S.SPACE_5),
        bgcolor=C.SURFACE,
        border=ft.border.all(1, C.BORDER),
        border_radius=R.RADIUS_LG,
        shadow=SH.SHADOW_SM,
        ink=True,
    )
    card.on_hover = _hover_elevation
    return card


def DonutStatus(data: Dict[str, int]) -> ft.Container:
    """Donut chart showing status distribution."""
    total = sum(data.values())
    colors_map = {
        "vigente": C.SUCCESS_TEXT,
        "a_vencer": C.WARNING_TEXT,
        "vencida": C.ERROR_TEXT,
    }
    sections = [
        ft.PieChartSection(value=v, color=colors_map[k], radius=80, title="")
        for k, v in data.items() if v > 0
    ]
    pie = ft.PieChart(
        sections=sections,
        sections_space=0,
        center_space_radius=60,
        expand=True,
    )
    center = ft.Column(
        [
            ft.Text(str(total), size=24, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY),
            ft.Text("Total", size=TY.TEXT_XS, color=C.TEXT_SECONDARY),
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    chart = ft.Stack(
        [pie, ft.Container(content=center, alignment=ft.alignment.center)],
        width=200,
        height=200,
    )
    legend_items = []
    for key, label, variant in [
        ("vigente", "Vigentes", "success"),
        ("a_vencer", "A Vencer", "warning"),
        ("vencida", "Vencidas", "error"),
    ]:
        count = data.get(key, 0)
        pct = (count / total * 100) if total else 0
        legend_items.append(StatusBadge(f"{label} {count} ({pct:.0f}%)", variant))
    legend = ft.Row(legend_items, spacing=S.SPACE_3)
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Situação das Atas",
                    size=TY.TEXT_LG,
                    weight=ft.FontWeight.W_600,
                    color=C.TEXT_PRIMARY,
                ),
                chart,
                legend,
            ],
            spacing=S.SPACE_4,
        ),
        padding=ft.padding.all(S.SPACE_5),
        bgcolor=C.SURFACE,
        border=ft.border.all(1, C.BORDER),
        border_radius=R.RADIUS_LG,
        shadow=SH.SHADOW_SM,
        ink=True,
    )
    container.on_hover = _hover_elevation
    return container


def MonthlyBarChart(data: Dict[int, int]) -> ft.Container:
    """Bar chart showing monthly expirations."""
    month_names = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    max_y = max(data.values()) if data else 0
    bar_groups = []
    for i, name in enumerate(month_names, start=1):
        value = data.get(i, 0)
        color = fcolors.GREY_300
        if name == "Out":
            color = fcolors.ORANGE_400
        elif name == "Nov":
            color = fcolors.RED_400
        rod = ft.BarChartRod(from_y=0, to_y=value, width=14, color=color, border_radius=6)
        bar_groups.append(ft.BarChartGroup(x=i, bar_rods=[rod]))
    chart = ft.BarChart(
        bar_groups=bar_groups,
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=i + 1, label=ft.Text(name, size=TY.TEXT_XS))
                for i, name in enumerate(month_names)
            ]
        ),
        max_y=max_y + 1,
        border=ft.border.all(0, "transparent"),
        expand=True,
    )
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Vencimentos por Mês",
                    size=TY.TEXT_LG,
                    weight=ft.FontWeight.W_600,
                    color=C.TEXT_PRIMARY,
                ),
                chart,
            ],
            spacing=S.SPACE_4,
        ),
        padding=ft.padding.all(S.SPACE_5),
        bgcolor=C.SURFACE,
        border=ft.border.all(1, C.BORDER),
        border_radius=R.RADIUS_LG,
        shadow=SH.SHADOW_SM,
        ink=True,
    )
    container.on_hover = _hover_elevation
    return container

__all__ = ["AlertBanner", "MetricCard", "DonutStatus", "MonthlyBarChart"]
