import flet as ft
from typing import Callable, List

try:
    from .tokens import (
        SPACE_1,
        SPACE_2,
        SPACE_3,
        SPACE_4,
        SPACE_5,
        SPACE_6,
        build_card,
        primary_button,
    )
except Exception:  # pragma: no cover - fallback for standalone execution
    from tokens import (
        SPACE_1,
        SPACE_2,
        SPACE_3,
        SPACE_4,
        SPACE_5,
        SPACE_6,
        build_card,
        primary_button,
    )

try:
    from ..models.ata import Ata
    from ..utils.validators import Formatters
    from ..utils.chart_utils import ChartUtils
except ImportError:  # for standalone execution
    from models.ata import Ata
    from utils.validators import Formatters
    from utils.chart_utils import ChartUtils


STATUS_INFO = {
    "vigente": {
        "title": "Atas Vigentes",
        "filter": "Vigentes",
        "icon": ft.icons.CHECK_CIRCLE,
        "icon_color": "#16A34A",
        "icon_bg": "#D1FAE5",
        "button_color": ft.colors.GREEN,
    },
    "a_vencer": {
        "title": "Atas a Vencer",
        "filter": "A Vencer",
        "icon": ft.icons.WARNING_AMBER_ROUNDED,
        "icon_color": "#CA8A04",
        "icon_bg": "#FEF9C3",
        "button_color": ft.colors.ORANGE,
    },
    "vencida": {
        "title": "Atas Vencidas",
        "filter": "Vencidas",
        "icon": ft.icons.CANCEL,
        "icon_color": "#DC2626",
        "icon_bg": "#FEE2E2",
        "button_color": ft.colors.RED,
    },
    "todos": {
        "title": "Todas as Atas",
        "filter": "Todas",
        "icon": ft.icons.LIST,
        "icon_color": "#1D4ED8",
        "icon_bg": "#DBEAFE",
        "button_color": ft.colors.BLUE,
    },
}


def build_header(
    nova_ata_cb: Callable,
    verificar_alertas_cb: Callable,
    relatorio_semanal_cb: Callable,
    relatorio_mensal_cb: Callable,
    testar_email_cb: Callable,
    status_cb: Callable,
) -> ft.AppBar:
    """Return AppBar with menu actions and new ata button."""
    return ft.AppBar(
        leading=ft.Icon(ft.icons.DESCRIPTION_OUTLINED),
        leading_width=40,
        title=ft.Text("Ata de Registro de Preços"),
        bgcolor=ft.colors.INVERSE_PRIMARY,
        actions=[
            ft.PopupMenuButton(
                icon=ft.icons.SETTINGS,
                tooltip="Ferramentas",
                items=[
                    ft.PopupMenuItem(text="🔍 Verificar Alertas", on_click=verificar_alertas_cb),
                    ft.PopupMenuItem(text="📊 Relatório Semanal", on_click=relatorio_semanal_cb),
                    ft.PopupMenuItem(text="📈 Relatório Mensal", on_click=relatorio_mensal_cb),
                    ft.PopupMenuItem(text="📧 Testar Email", on_click=testar_email_cb),
                    ft.PopupMenuItem(text="ℹ️ Status Sistema", on_click=status_cb),
                ],
            ),
            primary_button(
                "Nova Ata",
                icon=ft.icons.ADD,
                on_click=nova_ata_cb,
            ),
        ],
    )


def build_filters(
    filtro_atual: str, filtro_cb: Callable[[str], None]
) -> List[ft.ElevatedButton]:
    """Return filter buttons following design specifications."""

    def button(
        label: str, value: str, info: dict[str, str]
    ) -> ft.ElevatedButton:
        bg = info["button_color"] if filtro_atual == value else ft.colors.SURFACE_VARIANT
        content = ft.Row(
            [
                ft.Icon(info["icon"], color=info.get("icon_color")),
                ft.Text(label, no_wrap=True, size=14, weight=ft.FontWeight.W_500),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        return ft.ElevatedButton(
            content=content,
            height=48,
            width=140,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=16),
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=bg,
            ),
            on_click=lambda e: filtro_cb(value),
        )

    buttons: List[ft.ElevatedButton] = []
    for key in ["vigente", "a_vencer", "vencida", "todos"]:
        info = STATUS_INFO[key]
        buttons.append(button(info["filter"], key, info))

    return buttons


def build_search(on_change: Callable, value: str = "") -> tuple[ft.Container, ft.TextField]:
    """Return a search container and field pre-populated with ``value``."""
    search_field = ft.TextField(
        prefix_icon=ft.icons.SEARCH,
        on_change=on_change,
        value=value,
        height=48,
        border_radius=8,
        content_padding=ft.padding.symmetric(horizontal=16),
        expand=True,
        hint_text="Buscar atas...",
    )
    container = ft.Container(content=search_field, width=320)
    return container, search_field


def build_data_table(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
    status: str,
) -> ft.DataTable:
    """Return DataTable for a list of atas respecting design specs."""

    columns = [
        ft.DataColumn(ft.Text("Número")),
        ft.DataColumn(ft.Text("Vigência")),
        ft.DataColumn(ft.Text("Objeto")),
        ft.DataColumn(ft.Text("Fornecedor")),
        ft.DataColumn(ft.Text("Situação")),
        ft.DataColumn(ft.Text("Ações")),
    ]

    badge_colors = {
        "vigente": ("#14532D", "#D1FAE5"),
        "a_vencer": ("#713F12", "#FEF9C3"),
        "vencida": ("#991B1B", "#FEE2E2"),
    }

    rows: list[ft.DataRow] = []
    for ata in atas:
        data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)
        badge_text_color, badge_bg_color = badge_colors[ata.status]
        badge = ft.Container(
            ft.Text(
                ata.status.replace("_", " ").title(),
                size=14,
                weight=ft.FontWeight.W_400,
                color=badge_text_color,
            ),
            padding=ft.padding.symmetric(vertical=4, horizontal=8),
            bgcolor=badge_bg_color,
            border_radius=6,
        )

        actions = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.VISIBILITY,
                    icon_size=20,
                    icon_color=ft.colors.GREY_600,
                    on_click=lambda e, ata=ata: visualizar_cb(ata),
                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_size=20,
                    icon_color=ft.colors.GREY_600,
                    on_click=lambda e, ata=ata: editar_cb(ata),
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_size=20,
                    icon_color=ft.colors.GREY_600,
                    on_click=lambda e, ata=ata: excluir_cb(ata),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(
                            ata.numero_ata,
                            size=14,
                            weight=ft.FontWeight.W_400,
                            no_wrap=True,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            data_formatada,
                            size=14,
                            weight=ft.FontWeight.W_400,
                            no_wrap=True,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            ata.objeto,
                            size=14,
                            weight=ft.FontWeight.W_400,
                            no_wrap=True,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            ata.fornecedor,
                            size=14,
                            weight=ft.FontWeight.W_400,
                            no_wrap=True,
                        )
                    ),
                    ft.DataCell(badge),
                    ft.DataCell(actions),
                ]
            )
        )

    table = ft.DataTable(
        columns=columns,
        rows=rows,
        column_spacing=24,
        expand=True,
    )
    return table


def build_grouped_data_tables(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
    filtro: str = "todos",
) -> ft.Container:
    """Return a single status card with the atas list respecting ``filtro``."""

    info = STATUS_INFO.get(filtro, STATUS_INFO["todos"])

    icon = ft.Container(
        content=ft.Icon(info["icon"], color=info["icon_color"], size=20),
        width=28,
        height=28,
        padding=ft.padding.all(SPACE_1),
        bgcolor=info["icon_bg"],
        border_radius=4,
    )

    table = build_data_table(atas, visualizar_cb, editar_cb, excluir_cb, filtro)

    card = build_card(info["title"], icon, table)

    return ft.Container(content=card, width="100%", margin=ft.margin.only(top=32))


def build_atas_vencimento(
    atas_vencimento: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    alerta_cb: Callable[[Ata], None],
) -> ft.Container:
    if not atas_vencimento:
        return ft.Container()

    items = []
    for ata in atas_vencimento:
        data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)
        item = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(f"Ata: {ata.numero_ata}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Vencimento: {data_formatada}"),
                    ft.Text(
                        f"Faltam {ata.dias_restantes} dias",
                        color=ft.colors.RED if ata.dias_restantes <= 30 else ft.colors.ORANGE,
                    ),
                ], spacing=4),
                ft.Row([
                    ft.IconButton(icon=ft.icons.VISIBILITY, tooltip="Visualizar", on_click=lambda e, ata=ata: visualizar_cb(ata)),
                    ft.IconButton(icon=ft.icons.EMAIL, tooltip="Enviar Alerta", on_click=lambda e, ata=ata: alerta_cb(ata)),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(SPACE_3),
            margin=ft.margin.only(bottom=SPACE_2),
            border=ft.border.all(1, ft.colors.ORANGE),
            border_radius=8,
            bgcolor=ft.colors.ORANGE_50,
        )
        items.append(item)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "🔔 Atas Próximas do Vencimento",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Column(items, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            spacing=SPACE_3,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(SPACE_4),
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=8,
    )


def build_stats_panel(ata_service) -> ft.Container:
    stats = ata_service.get_estatisticas()
    atas = ata_service.listar_todas()
    atas_vencimento = ata_service.get_atas_vencimento_proximo()
    total_value = sum(ata.valor_total for ata in atas)
    summary_cards = ChartUtils.create_summary_cards(stats, total_value)
    pie_chart = ChartUtils.create_status_pie_chart(stats)
    legend = ChartUtils.create_status_legend(stats)
    urgency_indicator = ChartUtils.create_urgency_indicator(atas_vencimento)
    value_chart = ChartUtils.create_value_chart(atas)
    monthly_chart = ChartUtils.create_monthly_chart(atas)

    chart_left = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "📊 Situação das Atas",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    [pie_chart, legend],
                    spacing=32,
                    alignment=ft.MainAxisAlignment.START,
                ),
                value_chart,
            ],
            spacing=SPACE_4,
        ),
        padding=ft.padding.all(SPACE_4),
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=8,
        expand=True,
    )
    chart_left.col = {"xs": 12, "lg": 8}
    chart_right = ft.Container(content=monthly_chart, width=360)
    chart_right.col = {"xs": 12, "lg": 4}
    charts_section = ft.ResponsiveRow(
        [chart_left, chart_right],
        columns=12,
        spacing=SPACE_4,
        run_spacing=SPACE_4,
    )

    return ft.Container(
        content=ft.Column(
            [urgency_indicator, summary_cards, charts_section], spacing=SPACE_4
        ),
        margin=ft.margin.only(bottom=SPACE_5),
    )
