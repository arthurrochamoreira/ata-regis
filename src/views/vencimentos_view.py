"""View listing Atas close to expiration."""
import flet as ft
from constants import SPACE_4

SAMPLE_VENCIMENTOS = [
    {"numero": "001/2024", "fornecedor": "Tech Ltda", "dias": 20},
    {"numero": "002/2024", "fornecedor": "Papelaria ABC", "dias": 10},
    {"numero": "003/2023", "fornecedor": "Serviços XYZ", "dias": 4},
]


def create_vencimentos_view(app) -> ft.ListView:
    items = []
    for ata in SAMPLE_VENCIMENTOS:
        dias = ata["dias"]
        if dias <= 5:
            color = ft.colors.RED
        elif dias <= 15:
            color = ft.colors.ORANGE
        else:
            color = ft.colors.GREY
        badge = ft.Container(
            bgcolor=color,
            border_radius=12,
            padding=ft.padding.symmetric(vertical=2, horizontal=6),
            content=ft.Text(f"{dias} dias", size=12, color=ft.colors.WHITE),
        )
        tile = ft.ListTile(
            title=ft.Text(f"{ata['numero']} – {ata['fornecedor']}")
            ,subtitle=badge,
            trailing=ft.Row(
                [
                    ft.TextButton("Detalhes", on_click=lambda e, a=ata: app.show_details(a)),
                    ft.TextButton("Enviar alerta"),
                ],
                spacing=SPACE_4,
            ),
        )
        items.append(tile)
    return ft.ListView(items, expand=True, spacing=SPACE_4)
