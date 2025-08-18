import flet as ft
from datetime import timedelta
from typing import Callable

from .theme.spacing import (
    SPACE_1,
    SPACE_2,
    SPACE_3,
    SPACE_4,
    SPACE_5,
    SPACE_6,
)
from .theme.shadows import SHADOW_LG
from .tokens import build_section, primary_button, secondary_button
from .theme import colors

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
                ft.Text(label, weight=ft.FontWeight.W_500, color=colors.SEM.muted, width=128),
                ft.Text(value, color=colors.SEM.text, expand=True),
            ]
        )

    header_buttons = ft.ResponsiveRow(
        [
            secondary_button(
                "Voltar",
                icon=ft.icons.ARROW_BACK_ROUNDED,
                on_click=on_back,
                expand=True,
                col={"xs": 12, "md": 6},
            ),
            primary_button(
                "Editar",
                icon=ft.icons.EDIT_OUTLINED,
                on_click=on_edit,
                expand=True,
                col={"xs": 12, "md": 6},
            ),
        ],
        columns=12,
        spacing=SPACE_3,
        run_spacing=SPACE_3,
        alignment=ft.MainAxisAlignment.END,
    )

    header = ft.ResponsiveRow(
        [
            ft.Column(
                spacing=SPACE_1,
                controls=[
                    ft.Text(
                        "Ata de Registro de Preços",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=colors.SEM.text,
                    ),
                    ft.Text(f"Nº {ata.numero_ata}", size=16, color=colors.SEM.muted),
                ],
                col={"xs": 12, "md": 6},
            ),
            header_buttons,
        ],
        columns=12,
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
                color=colors.SEM.muted,
            ),
            ft.Row(
                [
                    ft.Icon(ft.icons.CHECK_CIRCLE, color=colors.SEM.success_text),
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
                    ft.Icon(ft.icons.CALENDAR_MONTH, color=colors.SEM.error_text),
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
        colors.SEM.primary,
        ft.colors.with_opacity(0.15, colors.SEM.primary),
        dados_gerais_body,
    )

    item_rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Container(
                        ft.Text(
                            item.descricao,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    )
                ),
                ft.DataCell(
                    ft.Container(
                        ft.Text(
                            str(item.quantidade),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    )
                ),
                ft.DataCell(
                    ft.Container(
                        ft.Text(
                            Formatters.formatar_valor_monetario(item.valor),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    )
                ),
                ft.DataCell(
                    ft.Container(
                        ft.Text(
                            Formatters.formatar_valor_monetario(item.valor_total),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    )
                ),
            ]
        )
        for item in ata.itens
    ]

    itens_table = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Container(
                    ft.Text(
                        "Descrição",
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                )
            ),
            ft.DataColumn(
                ft.Container(
                    ft.Text(
                        "Qtd.",
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                )
            ),
            ft.DataColumn(
                ft.Container(
                    ft.Text(
                        "Valor Unit.",
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                )
            ),
            ft.DataColumn(
                ft.Container(
                    ft.Text(
                        "Subtotal",
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                )
            ),
        ],
        rows=item_rows,
        heading_row_height=32,
        data_row_min_height=32,
        column_spacing=SPACE_3,
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
        bgcolor=ft.colors.with_opacity(0.05, colors.SEM.primary),
        padding=SPACE_4,
        border_radius=8,
    )

    itens_body = ft.Column([itens_table, resumo_financeiro], spacing=SPACE_5)
    itens_section = build_section(
        "Itens da Ata",
        ft.icons.LIST_ALT_OUTLINED,
        colors.SEM.primary,
        ft.colors.with_opacity(0.15, colors.SEM.primary),
        itens_body,
    )

    fornecedor_body = ft.Column([ft.Text(ata.fornecedor, size=18)], spacing=SPACE_4)
    fornecedor_section = build_section(
        "Fornecedor",
        ft.icons.BUSINESS_OUTLINED,
        colors.SEM.warning_text,
        colors.SEM.warning_bg,
        fornecedor_body,
    )

    contatos_list = []
    for tel in ata.telefones_fornecedor:
        contatos_list.append(
            ft.Row(
                [
                    ft.Icon(ft.icons.PHONE_OUTLINED, color=colors.SEM.muted),
                    ft.Text(tel),
                ],
                spacing=SPACE_2,
            )
        )
    if ata.telefones_fornecedor:
        contatos_list.append(ft.Divider(height=1, color=colors.SEM.border))
    for email in ata.emails_fornecedor:
        contatos_list.append(
            ft.Row(
                [
                    ft.Icon(ft.icons.EMAIL_OUTLINED, color=colors.SEM.muted),
                    ft.Text(email),
                ],
                spacing=SPACE_2,
            )
        )

    contatos_body = ft.Column(contatos_list, spacing=SPACE_3)
    contatos_section = build_section(
        "Contatos",
        ft.icons.HEADSET_MIC_OUTLINED,
        colors.SEM.primary,
        ft.colors.with_opacity(0.15, colors.SEM.primary),
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
            spacing=SPACE_6,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        bgcolor=colors.SEM.surface,
        padding=ft.padding.only(
            left=SPACE_5,
            right=SPACE_5,
            top=SPACE_4,
            bottom=SPACE_4,
        ),
        border_radius=8,
        alignment=ft.alignment.center,
        shadow=SHADOW_LG,
        expand=True,
        width=1152,
    )

    return card
