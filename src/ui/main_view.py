import flet as ft
from typing import Callable, List

try:
    from ..models.ata import Ata
    from ..utils.validators import Formatters
    from ..utils.chart_utils import ChartUtils
except ImportError:  # for standalone execution
    from models.ata import Ata
    from utils.validators import Formatters
    from utils.chart_utils import ChartUtils


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
            ft.ElevatedButton(
                "➕ Nova Ata",
                on_click=nova_ata_cb,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            ),
        ],
    )


def build_filters(filtro_atual: str, filtro_cb: Callable[[str], None]) -> ft.Container:
    """Return container with filter buttons."""
    def button(label: str, value: str, color: str) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            label,
            on_click=lambda e: filtro_cb(value),
            bgcolor=color if filtro_atual == value else ft.colors.SURFACE_VARIANT,
        )

    return ft.Container(
        content=ft.Row(
            [
                button("✅ Vigentes", "vigente", ft.colors.GREEN),
                button("⚠️ A Vencer", "a_vencer", ft.colors.ORANGE),
                button("❌ Vencidas", "vencida", ft.colors.RED),
                button("📋 Todas", "todos", ft.colors.BLUE),
            ],
            spacing=10,
        ),
        padding=ft.padding.all(16),
        margin=ft.margin.only(bottom=16),
        expand=True,
    )


def build_search(on_change: Callable, value: str = "") -> tuple[ft.Container, ft.TextField]:
    """Return a search container and field pre-populated with ``value``."""
    search_field = ft.TextField(
        label="Buscar atas...",
        prefix_icon=ft.icons.SEARCH,
        on_change=on_change,
        value=value,
        expand=True,
    )
    return (
        ft.Container(
            content=search_field,
            padding=ft.padding.all(16),
            margin=ft.margin.only(bottom=16),
            expand=True,
        ),
        search_field,
    )


def build_data_table(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
    status: str,
) -> ft.Column:
    """Return custom table for a list of atas respecting design specs."""

    header_labels = ["Número", "Vigência", "Objeto", "Fornecedor", "Situação", "Ações"]

    header_cells = [
        ft.Container(
            ft.Text(lbl.upper(), size=12, weight=ft.FontWeight.W_600, color="#6B7280"),
            expand=1,
        )
        for lbl in header_labels
    ]
    header_row = ft.Container(
        content=ft.Row(header_cells, spacing=16),
        padding=ft.padding.symmetric(vertical=12, horizontal=16),
        bgcolor="#F9FAFB",
        border=ft.border.only(bottom=ft.BorderSide(1, "#E5E7EB")),
    )

    badge_colors = {
        "vigente": ("#14532D", "#D1FAE5"),
        "a_vencer": ("#713F12", "#FEF9C3"),
        "vencida": ("#991B1B", "#FEE2E2"),
    }

    rows: list[ft.Control] = []
    total = len(atas)
    for index, ata in enumerate(atas):
        data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)
        text_cells = [
            ft.Text(
                ata.numero_ata,
                weight=ft.FontWeight.W_500,
                color="#111827",
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
            ft.Text(data_formatada, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
            ft.Text(
                ata.objeto,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
            ft.Text(
                ata.fornecedor,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
        ]
        badge_text_color, badge_bg_color = badge_colors[ata.status]
        badge = ft.Container(
            ft.Text(ata.status.replace("_", " ").title(), size=12, weight=ft.FontWeight.W_500, color=badge_text_color),
            padding=ft.padding.symmetric(vertical=2, horizontal=8),
            bgcolor=badge_bg_color,
            border_radius=6,
        )

        actions = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.VISIBILITY,
                    tooltip="Visualizar",
                    on_click=lambda e, ata=ata: visualizar_cb(ata),
                    style=ft.ButtonStyle(
                        color={ft.MaterialState.HOVERED: "#2563EB", "": "#6B7280"}
                    ),
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    tooltip="Editar",
                    on_click=lambda e, ata=ata: editar_cb(ata),
                    style=ft.ButtonStyle(
                        color={ft.MaterialState.HOVERED: "#CA8A04", "": "#6B7280"}
                    ),
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    tooltip="Excluir",
                    on_click=lambda e, ata=ata: excluir_cb(ata),
                    style=ft.ButtonStyle(
                        color={ft.MaterialState.HOVERED: "#DC2626", "": "#6B7280"}
                    ),
                    icon_size=20,
                ),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        cells = [
            ft.Container(text_cells[0], expand=1),
            ft.Container(text_cells[1], expand=1),
            ft.Container(text_cells[2], expand=2),
            ft.Container(text_cells[3], expand=1),
            ft.Container(badge, expand=1),
            ft.Container(actions, expand=1),
        ]

        row_container = ft.Container(
            content=ft.Row(cells, spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(16),
            border=ft.border.only(bottom=ft.BorderSide(1, "#E5E7EB")) if index < total - 1 else None,
        )

        rows.append(row_container)

    body = ft.Column(rows, spacing=0)

    table = ft.Container(
        content=ft.Column([header_row, body], spacing=0),
        border=ft.border.all(1, "#E5E7EB"),
        119uxv-codex/ajuste-layout-tela-de-atas
        clip_behavior=ft.ClipBehavior.HARD_EDGE,

    )

    return table


def build_grouped_data_tables(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
) -> ft.Container:
    """Return layout with status cards for the given atas."""

    groups: dict[str, list[Ata]] = {"vigente": [], "a_vencer": [], "vencida": []}
    for ata in atas:
        groups[ata.status].append(ata)

    status_info = {
        "vigente": {
            "title": "Atas Vigentes",
            "icon": ft.icons.CHECK_CIRCLE,
            "icon_color": "#16A34A",
            "icon_bg": "#D1FAE5",
        },
        "a_vencer": {
            "title": "Atas a Vencer",
            "icon": ft.icons.WARNING_AMBER_ROUNDED,
            "icon_color": "#CA8A04",
            "icon_bg": "#FEF9C3",
        },
        "vencida": {
            "title": "Atas Vencidas",
            "icon": ft.icons.CANCEL,
            "icon_color": "#DC2626",
            "icon_bg": "#FEE2E2",
        },
    }

    card_controls = []
    for status in ["vigente", "a_vencer", "vencida"]:
        atas_status = groups[status]

        header = ft.Row(
            [
                ft.Container(
                    content=ft.Icon(status_info[status]["icon"], color=status_info[status]["icon_color"], size=20),
                    width=28,
                    height=28,
                    padding=ft.padding.all(4),
                    bgcolor=status_info[status]["icon_bg"],
                    border_radius=4,
                ),
                ft.Text(
                    status_info[status]["title"],
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#1F2937",
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        table = build_data_table(
            atas_status,
            visualizar_cb,
            editar_cb,
            excluir_cb,
            status,
        )

        card = ft.Container(
            content=ft.Column([header, table], spacing=24),
            bgcolor="#FFFFFF",
            padding=24,
            shadow=ft.BoxShadow(spread_radius=-1, blur_radius=6, color=ft.colors.with_opacity(0.1, ft.colors.BLACK), offset=ft.Offset(0, 4)),
            width=float("inf"),
        )
        card.col = {"xs": 12, "lg": 4}
        card_controls.append(card)

    row = ft.ResponsiveRow(
        card_controls,
        columns=12,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=24,
        run_spacing=24,
    )

    container = ft.Container(
        content=row,
        alignment=ft.alignment.center,
        padding=0,
        expand=True,
    )
    return container


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
            padding=ft.padding.all(12),
            margin=ft.margin.only(bottom=8),
            border=ft.border.all(1, ft.colors.ORANGE),
            border_radius=8,
            bgcolor=ft.colors.ORANGE_50,
        )
        items.append(item)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("🔔 Atas Próximas do Vencimento", size=18, weight=ft.FontWeight.BOLD),
                ft.Column(items, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(16),
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

    charts_section = ft.Row(
        [
            ft.Container(
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
                    spacing=16,
                ),
                padding=ft.padding.all(16),
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=8,
                expand=True,
            ),
            ft.Container(content=monthly_chart, width=360),
        ],
        spacing=16,
    )

    return ft.Container(
        content=ft.Column(
            [urgency_indicator, summary_cards, charts_section], spacing=16
        ),
        margin=ft.margin.only(bottom=24),
    )
