import datetime
import flet as ft

try:
    from services.ata_service import AtaService
except ImportError:  # pragma: no cover - package relative import
    from ..services.ata_service import AtaService

try:
    from ui.theme import Theme
except ImportError:  # pragma: no cover - package relative import
    from .ui.theme import Theme


def calcular_status(vigencia: datetime.date) -> str:
    hoje = datetime.date.today()
    if vigencia < hoje:
        return "Vencida"
    dias = (vigencia - hoje).days
    return "A vencer" if dias < 90 else "Vigente"


def badge_status(status: str) -> ft.Container:
    cor = {
        "Vigente": Theme.BLUE,
        "A vencer": Theme.YELLOW,
        "Vencida": Theme.ORANGE,
    }[status]
    return ft.Container(
        content=ft.Text(status, size=12, weight="bold", color=Theme.LIGHT),
        bgcolor=cor,
        border_radius=20,
        padding=ft.Padding(8, 4, 8, 4),
    )


def side_menu(selected: str, page: ft.Page):
    itens = [
        ("Dashboard", ft.icons.DASHBOARD_OUTLINED),
        ("Atas", ft.icons.LIBRARY_BOOKS_OUTLINED),
        ("Configurações", ft.icons.SETTINGS_OUTLINED),
    ]
    rows = []
    for rotulo, icone in itens:
        ativo = rotulo == selected
        rows.append(
            ft.Container(
                bgcolor=Theme.GREY if ativo else Theme.LIGHT,
                border_radius=ft.border_radius.only(top_left=48, bottom_left=48),
                padding=4,
                content=ft.Row(
                    controls=[
                        ft.Icon(name=icone, color=Theme.BLUE if ativo else Theme.DARK),
                        ft.Text(rotulo, visible=not page.drawer_open),
                    ],
                    vertical_alignment="center",
                ),
                on_click=lambda e, r=rotulo: print(f"trocar para {r}"),
            )
        )
    return rows


def main(page: ft.Page):
    page.title = "ARP Dashboard"
    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap",
        "Lato": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
    }
    page.bgcolor = Theme.GREY
    page.vertical_alignment = "start"

    ata_service = AtaService()
    atas = ata_service.listar_todas()

    drawer = ft.Container(
        width=280,
        bgcolor=Theme.LIGHT,
        content=ft.Column(
            controls=[
                ft.Container(
                    padding=ft.Padding(0, 24),
                    height=56,
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.DESCRIPTION_OUTLINED, color=Theme.BLUE),
                            ft.Text(
                                "ARP\u00a0Dashboard",
                                size=20,
                                weight="bold",
                                color=Theme.BLUE,
                                font_family=Theme.FONT_TITLE,
                            ),
                        ],
                        vertical_alignment="center",
                    ),
                ),
                ft.Divider(height=1),
                *side_menu("Dashboard", page),
                ft.Expander(visible=False),
                ft.Container(
                    padding=ft.Padding(12, 4),
                    content=ft.Row(
                        [ft.Icon(ft.icons.LOGOUT, color=Theme.RED), ft.Text("Sair", color=Theme.RED)],
                        vertical_alignment="center",
                    ),
                ),
            ],
            spacing=10,
            scroll="adaptive",
        ),
    )

    navbar = ft.Container(
        height=56,
        bgcolor=Theme.LIGHT,
        padding=ft.Padding(24, 0),
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.MENU,
                    on_click=lambda e: setattr(page, "drawer_open", not getattr(page, "drawer_open", False)),
                ),
                ft.TextField(
                    hint_text="Buscar atas...",
                    width=300,
                    height=36,
                    border_radius=36,
                    bgcolor=Theme.GREY,
                    content_padding=ft.Padding(16, 0, 0, 0),
                ),
                ft.Row(expand=True),
                ft.Stack(
                    controls=[
                        ft.Icon(ft.icons.NOTIFICATIONS_OUTLINED, size=24),
                        ft.CircleAvatar(
                            radius=10,
                            bgcolor=Theme.RED,
                            content=ft.Text("3", size=10, weight="bold", color=Theme.LIGHT),
                            top=-4,
                            left=12,
                        ),
                    ]
                ),
                ft.CircleAvatar(bgcolor=Theme.BLUE, content=ft.Text("AA", color=Theme.LIGHT)),
            ],
            vertical_alignment="center",
            spacing=24,
        ),
    )

    vigentes = sum(1 for a in atas if calcular_status(a.data_vigencia) == "Vigente")
    a_vencer = sum(1 for a in atas if calcular_status(a.data_vigencia) == "A vencer")
    vencidas = sum(1 for a in atas if calcular_status(a.data_vigencia) == "Vencida")
    total = vigentes + a_vencer + vencidas

    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(value=vigentes, title=f"{vigentes} Vigentes", color=Theme.BLUE),
            ft.PieChartSection(value=a_vencer, title=f"{a_vencer} A vencer", color=Theme.YELLOW),
            ft.PieChartSection(value=vencidas, title=f"{vencidas} Vencidas", color=Theme.ORANGE),
        ],
        sections_space=6,
        center_space_radius=50,
        height=240,
        width=240,
    )

    linhas_tabela = []
    for ata in atas:
        status = calcular_status(ata.data_vigencia)
        linhas_tabela.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(ata.numero_ata)),
                    ft.DataCell(ft.Text(ata.data_vigencia.strftime("%d/%m/%Y"))),
                    ft.DataCell(ft.Text(ata.objeto)),
                    ft.DataCell(ft.Text(ata.fornecedor)),
                    ft.DataCell(badge_status(status)),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(icon=ft.icons.VISIBILITY_OUTLINED, tooltip="Ver"),
                                ft.IconButton(icon=ft.icons.EDIT_OUTLINED, tooltip="Editar"),
                            ],
                            spacing=0,
                        )
                    ),
                ]
            )
        )

    tabela_atas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Número")),
            ft.DataColumn(ft.Text("Vigência")),
            ft.DataColumn(ft.Text("Objeto")),
            ft.DataColumn(ft.Text("Fornecedor")),
            ft.DataColumn(ft.Text("Situação")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=linhas_tabela,
        heading_row_color=Theme.LIGHT,
        data_row_min_height=56,
        column_spacing=12,
        divider_thickness=0.5,
    )

    alertas = []
    for ata in atas:
        status = calcular_status(ata.data_vigencia)
        if status == "A vencer":
            dias = (ata.data_vigencia - datetime.date.today()).days
            alertas.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.WARNING_AMBER_OUTLINED, color=Theme.YELLOW),
                    title=ft.Text(f"Ata {ata.numero_ata} vence em {dias}\u00a0dias"),
                    subtitle=ft.Text(ata.data_vigencia.strftime("%d/%m/%Y")),
                    trailing=ft.IconButton(icon=ft.icons.EMAIL_OUTLINED, tooltip="Enviar alerta"),
                    bgcolor=Theme.GREY,
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            )
    lista_alertas = ft.Column(alertas, scroll="auto")

    main_content = ft.Container(
        padding=ft.Padding(24, 24, 24, 24),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Dashboard", size=32, weight="bold", font_family=Theme.FONT_TITLE),
                    ],
                    alignment="spaceBetween",
                ),
                ft.Row(
                    [
                        ft.Container(chart, expand=True),
                        ft.Container(
                            content=ft.Column(
                                controls=[ft.Text("Atas a Vencer", size=24, weight="600"), lista_alertas],
                                spacing=16,
                            ),
                            width=300,
                        ),
                    ],
                    spacing=24,
                ),
                ft.Divider(height=32, opacity=0),
                tabela_atas,
            ],
            spacing=24,
            expand=True,
        ),
    )

    root = ft.Row(
        expand=True,
        controls=[
            drawer,
            ft.Column(
                controls=[navbar, main_content],
                expand=True,
            ),
        ],
        spacing=0,
    )

    page.add(root)


if __name__ == "__main__":
    ft.app(target=main)
