import flet as ft
from datetime import timedelta
from typing import Callable

try:
    from .tokens import (
        SPACE_1,
        SPACE_2,
        SPACE_3,
        SPACE_4,
        SPACE_5,
        SPACE_6,
        build_section,
        primary_button,
        secondary_button,
    )
except Exception:  # pragma: no cover
    from tokens import (
        SPACE_1,
        SPACE_2,
        SPACE_3,
        SPACE_4,
        SPACE_5,
        SPACE_6,
        build_section,
        primary_button,
        secondary_button,
    )

try:
    from ..models.ata import Ata
    from ..utils.validators import Formatters
    from .atas_table import AtasTable
except ImportError:  # standalone execution
    from models.ata import Ata
    from utils.validators import Formatters
    from atas_table import AtasTable


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
                spacing=SPACE_3,
                controls=[
                    secondary_button(
                        "Voltar",
                        icon=ft.icons.ARROW_BACK_ROUNDED,
                        on_click=on_back,
                    ),
                    primary_button(
                        "Editar",
                        icon=ft.icons.EDIT_OUTLINED,
                        on_click=on_edit,
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

    dados_gerais_body = ft.Column(
        [
            ft.Column(
                [info_row("Documento SEI:", ata.documento_sei), info_row("Objeto:", ata.objeto)],
                spacing=SPACE_4,
            ),
            timeline,
        ],
        spacing=SPACE_5,
    )
    dados_gerais = build_section(
        "Dados Gerais",
        ft.icons.DESCRIPTION_OUTLINED,
        "#4F46E5",
        "#E0E7FF",
        dados_gerais_body,
    )

    item_rows: list[dict] = []
    for item in ata.itens:
        item_rows.append(
            {
                "values": [
                    item.descricao,
                    str(item.quantidade),
                    Formatters.formatar_valor_monetario(item.valor),
                    Formatters.formatar_valor_monetario(item.valor_total),
                ]
            }
        )

    itens_table = AtasTable(
        ["Descrição", "Qtd.", "Valor Unit.", "Subtotal"],
        item_rows,
        page_width=1000,
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
        padding=SPACE_4,
        border_radius=8,
    )

    itens_body = ft.Column([itens_table, resumo_financeiro], spacing=SPACE_5)
    itens_section = build_section(
        "Itens da Ata",
        ft.icons.LIST_ALT_OUTLINED,
        "#4F46E5",
        "#E0E7FF",
        itens_body,
    )

    fornecedor_body = ft.Column([ft.Text(ata.fornecedor, size=18)], spacing=SPACE_4)
    fornecedor_section = build_section(
        "Fornecedor",
        ft.icons.BUSINESS_OUTLINED,
        "#EA580C",
        "#FFEDD5",
        fornecedor_body,
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

    contatos_body = ft.Column(contatos_list, spacing=12)
    contatos_section = build_section(
        "Contatos",
        ft.icons.HEADSET_MIC_OUTLINED,
        "#0F766E",
        "#CCFBF1",
        contatos_body,
    )

    layout = ft.Row(
        [
            ft.Column([dados_gerais, itens_section], spacing=SPACE_5, expand=2),
            ft.Column([fornecedor_section, contatos_section], spacing=SPACE_5, expand=1),
        ],
        spacing=SPACE_6,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    card = ft.Container(
        content=ft.Column(
            [header, layout],
            spacing=32,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        width=1152,
        bgcolor="#FFFFFF",
        padding=SPACE_5,
        border_radius=16,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
            offset=ft.Offset(0, 5),
        ),
        expand=True,
    )

    return card
