"""Form dialog for creating or editing an Ata."""
import flet as ft
from constants import SPACE_3, SPACE_4


def create_ata_form(on_cancel, on_save) -> ft.AlertDialog:
    """Return an AlertDialog containing Ata form."""
    numero = ft.TextField(label="Número")
    vigencia_inicio = ft.TextField(label="Início", width=150)
    vigencia_fim = ft.TextField(label="Fim", width=150)
    objeto = ft.TextField(label="Objeto", expand=True)
    fornecedor = ft.TextField(label="Fornecedor")
    status = ft.Dropdown(
        label="Status",
        options=[
            ft.dropdown.Option("Vigente"),
            ft.dropdown.Option("À Vencer"),
            ft.dropdown.Option("Vencida"),
        ],
    )

    content = ft.Card(
        content=ft.Container(
            ft.Column(
                [
                    ft.Row([numero], spacing=SPACE_3),
                    ft.Row([vigencia_inicio, vigencia_fim], spacing=SPACE_3),
                    objeto,
                    fornecedor,
                    status,
                ],
                spacing=SPACE_4,
                expand=True,
            ),
            padding=SPACE_4,
        )
    )

    dialog = ft.AlertDialog(
        modal=True,
        content=content,
        actions=[
            ft.TextButton("Cancelar", icon=ft.icons.CLOSE, on_click=on_cancel),
            ft.ElevatedButton("Salvar", icon=ft.icons.SAVE, on_click=lambda e: on_save({
                "numero": numero.value,
                "vigencia": f"{vigencia_inicio.value} - {vigencia_fim.value}",
                "objeto": objeto.value,
                "fornecedor": fornecedor.value,
                "status": status.value,
            })),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dialog
