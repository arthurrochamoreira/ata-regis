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
        leading=ft.Icon(
            ft.icons.DESCRIPTION_OUTLINED, semantic_label="Aplicação Ata de Registro de Preços"
        ),
        leading_width=40,
        title=ft.Text("Ata de Registro de Preços"),
        bgcolor=ft.colors.INVERSE_PRIMARY,
        actions=[
            ft.PopupMenuButton(
                icon=ft.icons.SETTINGS,
                tooltip="Ferramentas",
                semantic_label="Ferramentas",
                items=[
                    ft.PopupMenuItem(
                        text="🔍 Verificar Alertas", on_click=verificar_alertas_cb
                    ),
                    ft.PopupMenuItem(
                        text="📊 Relatório Semanal", on_click=relatorio_semanal_cb
                    ),
                    ft.PopupMenuItem(
                        text="📈 Relatório Mensal", on_click=relatorio_mensal_cb
                    ),
                    ft.PopupMenuItem(
                        text="📧 Testar Email", on_click=testar_email_cb
                    ),
                    ft.PopupMenuItem(
                        text="ℹ️ Status Sistema", on_click=status_cb
                    ),
                ],
            ),
            primary_button(
                "Nova Ata",
                icon=ft.Icon(ft.icons.ADD, semantic_label="Nova ata"),
                on_click=nova_ata_cb,
            ),
        ],
    )


def build_filters(filtro_atual: str, filtro_cb: Callable[[str], None]) -> ft.Row:
    """Return row with filter chips."""

    def chip(label: str, value: str, icon_name: str) -> ft.Container:
        selected = filtro_atual == value
        bg = ft.colors.INDIGO_600 if selected else ft.colors.GREY_200
        fg = ft.colors.WHITE if selected else ft.colors.BLACK87
        icon = ft.Icon(icon_name, size=16, color=fg, semantic_label=label)
        text = ft.Text(label, no_wrap=True, overflow="ellipsis", color=fg)
        return ft.Container(
            content=ft.Row(
                [icon, text], spacing=4, alignment="center", vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=110,
            padding=SPACE_2,
            bgcolor=bg,
            border_radius=8,
            on_click=lambda e: filtro_cb(value),
        )

    chips = [
        chip("Vigente", "vigente", ft.icons.CHECK_CIRCLE),
        chip("A Vencer", "a_vencer", ft.icons.WARNING_AMBER_ROUNDED),
        chip("Vencidas", "vencida", ft.icons.CANCEL),
        chip("Todas", "todos", ft.icons.LIST),
    ]

    return ft.Row(chips, spacing=SPACE_2, wrap=True)


def build_search(on_change: Callable, value: str = "") -> ft.TextField:
    """Return a search text field pre-populated with ``value``."""

    return ft.TextField(
        label="Buscar atas...",
        prefix=ft.Icon(ft.icons.SEARCH, semantic_label="Buscar"),
        on_change=on_change,
        value=value,
        expand=True,
        height=44,
        content_padding=ft.padding.symmetric(horizontal=SPACE_4),
    )


def build_data_table(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
    status: str,
) -> ft.DataTable:
    """Return a DataTable for a list of atas respecting design specs."""

    columns = [
        ft.DataColumn(
            ft.Text(
                "Número", no_wrap=True, style=ft.TextStyle(weight=ft.FontWeight.W_600)
            )
        ),
        ft.DataColumn(
            ft.Text(
                "Vigência", no_wrap=True, style=ft.TextStyle(weight=ft.FontWeight.W_600)
            )
        ),
        ft.DataColumn(
            ft.Text(
                "Objeto", no_wrap=True, style=ft.TextStyle(weight=ft.FontWeight.W_600)
            )
        ),
        ft.DataColumn(
            ft.Text(
                "Fornecedor", no_wrap=True, style=ft.TextStyle(weight=ft.FontWeight.W_600)
            )
        ),
        ft.DataColumn(
            ft.Text(
                "Situação", no_wrap=True, style=ft.TextStyle(weight=ft.FontWeight.W_600)
            )
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text(
                    "Ações",
                    no_wrap=True,
                    style=ft.TextStyle(weight=ft.FontWeight.W_600),
                ),
                width=80,
                alignment=ft.alignment.center,
            )
        ),
    ]

    badge_colors = {
        "vigente": (ft.colors.GREEN_800, ft.colors.GREEN_100),
        "a_vencer": (ft.colors.AMBER_800, ft.colors.AMBER_100),
        "vencida": (ft.colors.RED_800, ft.colors.RED_100),
    }

    rows: list[ft.DataRow] = []
    for ata in atas:
        data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)

        badge_fg, badge_bg = badge_colors.get(ata.status, (ft.colors.BLACK, ft.colors.GREY_200))
        badge = ft.Container(
            ft.Text(
                ata.status.replace("_", " ").title(),
                size=12,
                weight=ft.FontWeight.W_500,
                color=badge_fg,
                no_wrap=True,
            ),
            padding=4,
            bgcolor=badge_bg,
            border_radius=4,
        )

        actions = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.VISIBILITY,
                    tooltip="Visualizar",
                    semantic_label="Visualizar ata",
                    on_click=lambda e, ata=ata: visualizar_cb(ata),
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    tooltip="Editar",
                    semantic_label="Editar ata",
                    on_click=lambda e, ata=ata: editar_cb(ata),
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    tooltip="Excluir",
                    semantic_label="Excluir ata",
                    on_click=lambda e, ata=ata: excluir_cb(ata),
                    icon_size=20,
                ),
            ],
            alignment="center",
            spacing=SPACE_2,
        )

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(
                            ata.numero_ata,
                            no_wrap=True,
                            overflow="ellipsis",
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            data_formatada,
                            no_wrap=True,
                            overflow="ellipsis",
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            ata.objeto,
                            no_wrap=True,
                            overflow="ellipsis",
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            ata.fornecedor,
                            no_wrap=True,
                            overflow="ellipsis",
                        )
                    ),
                    ft.DataCell(badge),
                    ft.DataCell(
                        ft.Container(
                            actions, width=80, alignment=ft.alignment.center
                        )
                    ),
                ]
            )
        )

    return ft.DataTable(
        columns=columns,
        rows=rows,
        data_row_min_height=48,
        column_spacing=24,
    )


def build_grouped_data_tables(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
    filtro: str = "todos",
) -> ft.Container:
    """Return layout with status cards for the given ``atas`` respecting ``filtro``."""

    groups: dict[str, list[Ata]] = {"vigente": [], "a_vencer": [], "vencida": []}
    for ata in atas:
        groups[ata.status].append(ata)

    statuses = [filtro] if filtro != "todos" else ["vigente", "a_vencer", "vencida"]

    cards: list[ft.Control] = []
    for status in statuses:
        atas_status = groups[status]
        info = STATUS_INFO[status]

        header = ft.Row(
            [
                ft.Icon(
                    info["icon"],
                    color=info["icon_color"],
                    size=20,
                    semantic_label=info["title"],
                ),
                ft.Text(info["title"], weight=ft.FontWeight.W_600),
            ],
            spacing=SPACE_2,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        if atas_status:
            content = build_data_table(
                atas_status, visualizar_cb, editar_cb, excluir_cb, status
            )
            min_height = 120
        else:
            content = ft.Text(
                "Nenhuma ata encontrada",
                italic=True,
                color=ft.colors.GREY_600,
            )
            min_height = None

        card = ft.Container(
            content=ft.Column([header, content], spacing=SPACE_4),
            padding=SPACE_4,
            border_radius=8,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            min_height=min_height,
        )
        cards.append(card)

    grid = ft.GridView(
        max_extent=480,
        child_aspect_ratio=1.2,
        spacing=24,
        controls=cards,
        expand=True,
    )

    return ft.Container(content=grid, expand=True)


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
                    ft.IconButton(
                        icon=ft.icons.VISIBILITY,
                        tooltip="Visualizar",
                        semantic_label="Visualizar ata",
                        on_click=lambda e, ata=ata: visualizar_cb(ata),
                    ),
                    ft.IconButton(
                        icon=ft.icons.EMAIL,
                        tooltip="Enviar Alerta",
                        semantic_label="Enviar alerta",
                        on_click=lambda e, ata=ata: alerta_cb(ata),
                    ),
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
