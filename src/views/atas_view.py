"""Main Atas view with filters and tables."""
import flet as ft
from constants import SPACE_4, SPACE_5
from widgets.badges import status_badge

SAMPLE_ATAS = [
    {
        "numero": "001/2024",
        "vigencia": "01/01/2024 - 31/12/2024",
        "objeto": "Serviços de TI",
        "fornecedor": "Tech Ltda",
        "status": "Vigente",
    },
    {
        "numero": "002/2024",
        "vigencia": "01/06/2024 - 31/05/2025",
        "objeto": "Materiais de escritório",
        "fornecedor": "Papelaria ABC",
        "status": "À Vencer",
    },
    {
        "numero": "003/2023",
        "vigencia": "01/01/2023 - 31/12/2023",
        "objeto": "Manutenção",
        "fornecedor": "Serviços XYZ",
        "status": "Vencida",
    },
]


STATUSES = ["Vigente", "À Vencer", "Vencida", "Todas"]


def create_atas_view(app) -> ft.Column:
    """Return Atas view with filters and tables."""
    filtro = getattr(app, "filtro", "Todas")

    def set_filtro(value):
        app.filtro = value
        app.render_view()
        app.page.update()

    chips = ft.Row(
        [
            ft.FilterChip(
                text=status,
                selected=filtro == status,
                on_select=lambda e, s=status: set_filtro(s),
            )
            for status in STATUSES
        ],
        spacing=SPACE_4,
    )

    search = ft.TextField(
        hint_text="Buscar...",
        prefix_icon=ft.icons.SEARCH,
        border_radius=15,
        expand=True,
        on_change=lambda e: None,
    )

    def build_table(status: str):
        data = [a for a in SAMPLE_ATAS if status == "Todas" or a["status"] == status]
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Número")),
                ft.DataColumn(ft.Text("Vigência")),
                ft.DataColumn(ft.Text("Objeto")),
                ft.DataColumn(ft.Text("Fornecedor")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(a["numero"])),
                        ft.DataCell(ft.Text(a["vigencia"])),
                        ft.DataCell(ft.Text(a["objeto"])),
                        ft.DataCell(ft.Text(a["fornecedor"])),
                        ft.DataCell(status_badge(a["status"])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(ft.icons.REMOVE_RED_EYE, on_click=lambda e, ata=a: app.show_details(ata)),
                                    ft.IconButton(ft.icons.EDIT),
                                    ft.IconButton(ft.icons.DELETE),
                                ],
                                spacing=SPACE_4,
                            )
                        ),
                    ]
                )
                for a in data
            ],
        )

    tables = []
    if filtro == "Todas":
        for st in STATUSES[:-1]:
            tables.append(build_table(st))
    else:
        tables.append(build_table(filtro))

    tables_controls = []
    for t in tables:
        tables_controls.append(t)
        tables_controls.append(ft.Container(height=SPACE_5))
    if tables_controls:
        tables_controls.pop()  # remove last spacer

    return ft.Column([chips, search] + tables_controls, spacing=SPACE_5, expand=True)
