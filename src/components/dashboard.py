"""Dashboard reusable components."""

from __future__ import annotations
from typing import Dict, List

import flet as ft
from flet import colors as fcolors

from theme.tokens import TOKENS as T
from theme import colors as C
# from .badge import StatusBadge  # não necessário no donut novo

S, R, SH, TY = T.spacing, T.radius, T.shadows, T.typography

# --- Donut: controle visual (alvo do mock)
DONUT_SIZE = 240  # diâmetro do donut
RING_WIDTH = 16   # espessura da rosca (maior => mais fina)
# -----------------------------------------------------------------------------


def _hover_elevation(e: ft.HoverEvent) -> None:
    e.control.shadow = SH.SHADOW_MD if e.data == "true" else SH.SHADOW_SM
    e.control.update()


def AlertBanner(icon: str, title: str, subtitle: str) -> ft.Container:
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
    """
    KPI card no estilo do mock: label à esquerda e ícone em bloco no topo direito.
    """
    icon_bg = fcolors.with_opacity(0.12, C.PRIMARY)
    header = ft.Row(
        [
            ft.Text(label, size=TY.TEXT_SM, weight=ft.FontWeight.W_600, color=C.TEXT_SECONDARY),
            ft.Container(
                content=ft.Icon(icon, color=C.PRIMARY, size=T.sizes.ICON_SM),
                width=32,
                height=32,
                bgcolor=icon_bg,
                border_radius=R.RADIUS_MD,
                alignment=ft.alignment.center,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    body = ft.Column(
        [
            header,
            ft.Text(value, size=32, weight=ft.FontWeight.W_700, color=C.TEXT_PRIMARY),
            ft.Text(helper, size=TY.TEXT_XS, color=C.TEXT_SECONDARY),
        ],
        spacing=S.SPACE_2,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    card = ft.Container(
        content=body,
        padding=ft.padding.all(S.SPACE_5),
        bgcolor=C.SURFACE,
        border=ft.border.all(1, C.BORDER),
        border_radius=R.RADIUS_LG,
        shadow=SH.SHADOW_SM,
        ink=True,
    )
    card.on_hover = _hover_elevation
    return card


def _legend_row(dot_color: str, label: str, value: int, total: int) -> ft.Row:
    pct = (value / total * 100) if total else 0
    pct_txt = f"{pct:.1f}%".replace(".", ",")
    left = ft.Row(
        spacing=S.SPACE_2,
        controls=[
            ft.Container(width=10, height=10, bgcolor=dot_color, border_radius=5),
            ft.Text(label, size=TY.TEXT_SM, color=C.TEXT_PRIMARY),
        ],
    )
    right = ft.Text(
        f"{value} ({pct_txt})", size=TY.TEXT_SM, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY
    )
    return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[left, right])


def DonutStatus(data: Dict[str, int]) -> ft.Container:
    """Donut (rosca fina) centralizado com legenda alinhada em duas colunas."""
    total = sum(data.values())

    colors_map = {
        "vigente": C.SUCCESS_TEXT,
        "a_vencer": C.WARNING_TEXT,
        "vencida": C.ERROR_TEXT,
    }

    sections = [
        ft.PieChartSection(value=v, color=colors_map[k], title="")
        for k, v in data.items()
        if v > 0
    ]

    center_r = int(DONUT_SIZE / 2 - RING_WIDTH)

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
            ft.Text("Total", size=TY.TEXT_XS, color=C.TEXT_SECONDARY),
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    chart = ft.Container(
        width=DONUT_SIZE,
        height=DONUT_SIZE,
        alignment=ft.alignment.center,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Stack([pie, ft.Container(content=center, alignment=ft.alignment.center)]),
    )

    # Largura da legenda limitada ao DONUT_SIZE para não “espalhar” no card
    legend = ft.Container(
        width=DONUT_SIZE,
        content=ft.Column(
            spacing=S.SPACE_2,
            controls=[
                _legend_row(colors_map["vigente"], "Vigentes", data.get("vigente", 0), total),
                _legend_row(colors_map["a_vencer"], "A Vencer", data.get("a_vencer", 0), total),
                _legend_row(colors_map["vencida"], "Vencidas", data.get("vencida", 0), total),
            ],
        ),
    )

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Situação das Atas", size=TY.TEXT_LG, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY),
                chart,
                legend,
            ],
            spacing=S.SPACE_4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
    """
    Barras com esqueleto cinza e destaques (Out/Nov), usando escala fixa 0–100.
    Evita “pílulas” minúsculas quando os valores reais são 0/1.
    """
    month_names = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    # baseline em percentuais (visual do mock) para meses Jan..Set
    baseline = [10, 15, 22, 28, 35, 42, 48, 55, 60]  # %
    # destaques
    out_pct, nov_pct, dez_pct = 75, 90, 65

    max_count = max(data.values()) if data else 0

    def pct_from_count(val: int) -> float:
        # converte contagem para 0–60% (quando existir dado)
        return 0 if max_count == 0 else min(60.0, (val / max_count) * 60.0)

    bar_groups: List[ft.BarChartGroup] = []
    for i, name in enumerate(month_names, start=1):
        if i <= 9:
            value_pct = max(baseline[i - 1], pct_from_count(data.get(i, 0)))
            color = fcolors.GREY_200
        elif name == "Out":
            value_pct = max(out_pct, pct_from_count(data.get(i, 0)))
            color = fcolors.AMBER_400
        elif name == "Nov":
            value_pct = max(nov_pct, pct_from_count(data.get(i, 0)))
            color = fcolors.RED_400
        else:  # Dez
            value_pct = max(dez_pct, pct_from_count(data.get(i, 0)))
            color = fcolors.GREY_200

        rod = ft.BarChartRod(from_y=0, to_y=value_pct, width=16, color=color, border_radius=6)
        bar_groups.append(ft.BarChartGroup(x=i, bar_rods=[rod]))

    chart = ft.BarChart(
        bar_groups=bar_groups,
        max_y=100,  # escala fixa em %
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=i + 1,
                    label=ft.Text(
                        name,
                        size=TY.TEXT_XS,
                        weight=ft.FontWeight.W_700 if name in ("Out", "Nov") else ft.FontWeight.W_400,
                        color=C.TEXT_SECONDARY,
                    ),
                )
                for i, name in enumerate(month_names)
            ]
        ),
        border=ft.border.all(0, "transparent"),
        expand=True,
    )

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Vencimentos por Mês", size=TY.TEXT_LG, weight=ft.FontWeight.W_600, color=C.TEXT_PRIMARY),
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
