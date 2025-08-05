"""Detailed card for displaying Ata information."""
import flet as ft
from constants import SPACE_3, SPACE_4, SPACE_5
from .badges import status_badge


def create_details_card(ata: dict, on_back, on_edit) -> ft.Card:
    """Create card with Ata details."""
    header = ft.Row(
        [
            ft.IconButton(icon=ft.icons.SETTINGS_BACK, on_click=on_back),
            ft.Text(ata.get("numero", "Ata"), weight=ft.FontWeight.BOLD, expand=True),
            ft.IconButton(icon=ft.icons.EDIT, on_click=on_edit),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    timeline = ft.Timeline(
        controls=[
            ft.Text(f"Vigência: {ata.get('vigencia', '---')}")
        ]
    )

    itens_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Item")),
            ft.DataColumn(ft.Text("Quantidade")),
            ft.DataColumn(ft.Text("Unidade")),
            ft.DataColumn(ft.Text("Valor Unit.")),
            ft.DataColumn(ft.Text("Subtotal")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(i.get("descricao", ""))),
                    ft.DataCell(ft.Text(str(i.get("quantidade", "")))),
                    ft.DataCell(ft.Text(i.get("unidade", ""))),
                    ft.DataCell(ft.Text(str(i.get("valor", "")))),
                    ft.DataCell(ft.Text(str(i.get("subtotal", "")))),
                ]
            )
            for i in ata.get("itens", [])
        ],
    )

    content = ft.Column(
        [
            header,
            timeline,
            itens_table,
            ft.Row(
                [
                    ft.Text("Subtotal:"),
                    ft.Text(str(ata.get("subtotal", 0))),
                    ft.Text("Valor Total:"),
                    ft.Text(str(ata.get("total", 0))),
                ],
                spacing=SPACE_4,
            ),
        ],
        spacing=SPACE_5,
    )

    return ft.Card(content=ft.Container(content, padding=SPACE_4, width=920))
