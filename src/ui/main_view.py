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
) -> ft.Container:
    """Return header container with menu and new ata button."""
    return ft.Container(
        content=ft.Row([
            ft.Text("📝 Ata de Registro de Preços", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
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
            ], spacing=8),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.all(16),
        margin=ft.margin.only(bottom=16),
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
        content=ft.Row([
            button("✅ Vigentes", "vigente", ft.colors.GREEN),
            button("⚠️ A Vencer", "a_vencer", ft.colors.ORANGE),
            button("❌ Vencidas", "vencida", ft.colors.RED),
            button("📋 Todas", "todos", ft.colors.BLUE),
        ], spacing=10),
        padding=ft.padding.all(16),
        margin=ft.margin.only(bottom=16),
    )


def build_search(on_change: Callable) -> tuple[ft.Container, ft.TextField]:
    search_field = ft.TextField(
        label="Buscar atas...",
        prefix_icon=ft.icons.SEARCH,
        on_change=on_change,
        width=400,
    )
    return (
        ft.Container(content=search_field, padding=ft.padding.all(16), margin=ft.margin.only(bottom=16)),
        search_field,
    )


def build_data_table(
    atas: List[Ata],
    visualizar_cb: Callable[[Ata], None],
    editar_cb: Callable[[Ata], None],
    excluir_cb: Callable[[Ata], None],
) -> ft.Container:
    rows = []
    for ata in atas:
        status_icon = "✅" if ata.status == "vigente" else "⚠️" if ata.status == "a_vencer" else "❌"
        data_formatada = Formatters.formatar_data_brasileira(ata.data_vigencia)
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(ata.numero_ata)),
                ft.DataCell(ft.Text(data_formatada)),
                ft.DataCell(ft.Text(ata.objeto)),
                ft.DataCell(ft.Text(ata.fornecedor)),
                ft.DataCell(ft.Text(f"{status_icon} {ata.status.replace('_', ' ').title()}")),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(icon=ft.icons.VISIBILITY, tooltip="Visualizar", on_click=lambda e, ata=ata: visualizar_cb(ata)),
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, ata=ata: editar_cb(ata)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Excluir", on_click=lambda e, ata=ata: excluir_cb(ata)),
                    ], spacing=0)
                ),
            ]
        )
        rows.append(row)

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Número")),
            ft.DataColumn(ft.Text("Vigência")),
            ft.DataColumn(ft.Text("Objeto")),
            ft.DataColumn(ft.Text("Fornecedor")),
            ft.DataColumn(ft.Text("Situação")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=rows,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=8,
    )

    return ft.Container(
        content=ft.Column(
            [ft.Text("📋 Lista de Atas", size=18, weight=ft.FontWeight.BOLD), table],
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(16),
        margin=ft.margin.only(bottom=24),
    )


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
