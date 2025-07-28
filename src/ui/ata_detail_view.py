import flet as ft
from datetime import timedelta
from typing import Callable

try:
    from ..models.ata import Ata
    from ..utils.validators import Formatters
except ImportError:  # standalone execution
    from models.ata import Ata
    from utils.validators import Formatters


def build_ata_detail_view(
    ata: Ata,
    on_back: Callable[[ft.ControlEvent], None],
    on_edit: Callable[[ft.ControlEvent], None],
) -> ft.Container:
    """Return a detailed view for an ``Ata`` using the design specifications."""

    def info_row(label: str, value: str) -> ft.Row:
        return ft.Row(
            [
                ft.Text(label, weight=ft.FontWeight.W_500, color="#6B7280", width=128),
                ft.Text(value, color="#1F2937", expand=True),
            ]
        )

    header = ft.Row(
        [
            ft.Column(
                spacing=2,
                controls=[
                    ft.Text(
                        "Ata de Registro de Preços",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="#111827",
                    ),
                    ft.Text(f"Nº {ata.numero_ata}", size=16, color="#6B7280"),
                ],
            ),
            ft.Row(
                spacing=12,
                controls=[
                    ft.OutlinedButton(
                        text="Voltar",
                        icon=ft.icons.ARROW_BACK_ROUNDED,
                        on_click=on_back,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            color="#4B5563",
                            side=ft.BorderSide(1, "#D1D5DB"),
                        ),
                    ),
                    ft.ElevatedButton(
                        text="Editar",
                        icon=ft.icons.EDIT_OUTLINED,
                        on_click=on_edit,
                        bgcolor="#3B82F6",
                        color="#FFFFFF",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                    ),
                ],
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    inicio = ata.data_vigencia - timedelta(days=365)

    timeline = ft.Column(
        spacing=0,
        controls=[
            ft.Text(
                "Linha do Tempo da Vigência",
                size=18,
                weight=ft.FontWeight.W_600,
                color="#374151",
            ),
            ft.Row(
                [
                    ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN),
                    ft.Column(
                        [
                            ft.Text("Início da vigência"),
                            ft.Text(
                                Formatters.formatar_data_brasileira(inicio)
                            ),
                        ],
                        spacing=0,
                    ),
                ]
            ),
            ft.Row(
                [
                    ft.Icon(ft.icons.CALENDAR_MONTH, color=ft.colors.RED),
                    ft.Column(
                        [
                            ft.Text("Fim da vigência"),
                            ft.Text(
                                Formatters.formatar_data_brasileira(
                                    ata.data_vigencia
                                )
                            ),
                        ],
                        spacing=0,
                    ),
                ]
            ),
        ],
    )

    dados_gerais = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.icons.DESCRIPTION_OUTLINED, color="#4F46E5"
                            ),
                            bgcolor="#E0E7FF",
                            padding=8,
                            border_radius=8,
                        ),
                        ft.Text(
                            "Dados Gerais",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1F2937",
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        info_row("Documento SEI:", ata.documento_sei),
                        info_row("Objeto:", ata.objeto),
                    ],
                    spacing=16,
                ),
                timeline,
            ],
            spacing=24,
        ),
        bgcolor="#F8FAFC",
        padding=24,
        border_radius=12,
    )

    item_rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(item.descricao)),
                ft.DataCell(ft.Text(str(item.quantidade))),
                ft.DataCell(ft.Text(Formatters.formatar_valor_monetario(item.valor))),
                ft.DataCell(
                    ft.Text(
                        Formatters.formatar_valor_monetario(item.valor_total)
                    )
                ),
            ]
        )
        for item in ata.itens
    ]

    itens_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Descrição", weight=ft.FontWeight.W_600)),
            ft.DataColumn(
                ft.Text("Qtd.", weight=ft.FontWeight.W_600), numeric=True
            ),
            ft.DataColumn(
                ft.Text("Valor Unit.", weight=ft.FontWeight.W_600), numeric=True
            ),
            ft.DataColumn(
                ft.Text("Subtotal", weight=ft.FontWeight.W_600), numeric=True
            ),
        ],
        rows=item_rows,
        heading_row_height=32,
        data_row_height=32,
        column_spacing=12,
    )

    resumo_financeiro = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Valor Total", weight=ft.FontWeight.W_600),
                ft.Text(
                    Formatters.formatar_valor_monetario(ata.valor_total),
                    weight=ft.FontWeight.W_600,
                ),
            ],
        ),
        bgcolor="#EEF2FF",
        padding=16,
        border_radius=8,
    )

    itens_section = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.icons.LIST_ALT_OUTLINED, color="#4F46E5"
                            ),
                            bgcolor="#E0E7FF",
                            padding=8,
                            border_radius=8,
                        ),
                        ft.Text(
                            "Itens da Ata",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1F2937",
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                itens_table,
                resumo_financeiro,
            ],
            spacing=24,
        ),
        bgcolor="#F8FAFC",
        padding=24,
        border_radius=12,
    )

    fornecedor_section = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.icons.BUSINESS_OUTLINED, color="#EA580C"
                            ),
                            bgcolor="#FFEDD5",
                            padding=8,
                            border_radius=8,
                        ),
                        ft.Text(
                            "Fornecedor",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1F2937",
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(ata.fornecedor, size=18),
            ],
            spacing=16,
        ),
        bgcolor="#F8FAFC",
        padding=24,
        border_radius=12,
    )

    contatos_list = []
    for tel in ata.telefones_fornecedor:
        contatos_list.append(
            ft.Row(
                [
                    ft.Icon(ft.icons.PHONE_OUTLINED, color="#6B7280"),
                    ft.Text(tel),
                ],
                spacing=8,
            )
        )
    if ata.telefones_fornecedor:
        contatos_list.append(ft.Divider(height=1, color="#9CA3AF"))
    for email in ata.emails_fornecedor:
        contatos_list.append(
            ft.Row(
                [
                    ft.Icon(ft.icons.EMAIL_OUTLINED, color="#6B7280"),
                    ft.Text(email),
                ],
                spacing=8,
            )
        )

    contatos_section = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.icons.HEADSET_MIC_OUTLINED, color="#0F766E"
                            ),
                            bgcolor="#CCFBF1",
                            padding=8,
                            border_radius=8,
                        ),
                        ft.Text(
                            "Contatos",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1F2937",
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(contatos_list, spacing=12),
            ],
            spacing=16,
        ),
        bgcolor="#F8FAFC",
        padding=24,
        border_radius=12,
    )

    layout = ft.Row(
        [
            ft.Column([dados_gerais, itens_section], spacing=24, expand=2),
            ft.Column([fornecedor_section, contatos_section], spacing=24, expand=1),
        ],
        spacing=32,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    card = ft.Container(
        content=ft.Column([header, layout], spacing=32),
        width=1152,
        bgcolor="#FFFFFF",
        padding=32,
        border_radius=16,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
            offset=ft.Offset(0, 5),
        ),
    )

    page_container = ft.Container(
        content=ft.Column([card], expand=True),
        padding=32,
        bgcolor="#F1F5F9",
        alignment=ft.alignment.top_center,
    )

    return page_container
