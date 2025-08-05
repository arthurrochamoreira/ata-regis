"""Dashboard view."""
import flet as ft
from constants import SPACE_4, SPACE_5


def create_dashboard(app) -> ft.Column:
    """Return dashboard layout."""
    urgency = ft.ProgressBar(value=0.3, expand=True)

    cards = ft.ResponsiveRow(
        controls=[
            ft.Container(
                ft.Card(ft.Container(ft.Text("Vigentes: 10"), padding=SPACE_4)),
                col={"xs": 12, "md": 6, "lg": 3},
            ),
            ft.Container(
                ft.Card(ft.Container(ft.Text("À vencer: 5"), padding=SPACE_4)),
                col={"xs": 12, "md": 6, "lg": 3},
            ),
            ft.Container(
                ft.Card(ft.Container(ft.Text("Vencidas: 2"), padding=SPACE_4)),
                col={"xs": 12, "md": 6, "lg": 3},
            ),
            ft.Container(
                ft.Card(ft.Container(ft.Text("Valor Total: 1M"), padding=SPACE_4)),
                col={"xs": 12, "md": 6, "lg": 3},
            ),
        ],
        spacing=SPACE_4,
    )

    pie = ft.PieChart(
        sections=[
            ft.PieChartSection(40, color=ft.colors.GREEN, title="Vigentes"),
            ft.PieChartSection(30, color=ft.colors.AMBER, title="À Vencer"),
            ft.PieChartSection(30, color=ft.colors.RED, title="Vencidas"),
        ],
        expand=True,
        height=200,
    )

    line = ft.LineChart(
        lines=[
            ft.LineChartData(
                data=[
                    ft.LineChartDataPoint(1, 10),
                    ft.LineChartDataPoint(2, 20),
                    ft.LineChartDataPoint(3, 40),
                ],
                color=ft.colors.BLUE,
            )
        ],
        expand=True,
        height=200,
    )

    bar = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(x=1, bar_rods=[ft.BarChartRod(from_y=0, to_y=10)]),
            ft.BarChartGroup(x=2, bar_rods=[ft.BarChartRod(from_y=0, to_y=20)]),
            ft.BarChartGroup(x=3, bar_rods=[ft.BarChartRod(from_y=0, to_y=15)]),
        ],
        expand=True,
        height=200,
    )

    charts = ft.ResponsiveRow(
        controls=[
            ft.Container(pie, col={"xs": 12, "md": 6, "lg": 4}),
            ft.Container(bar, col={"xs": 12, "md": 6, "lg": 4}),
            ft.Container(line, col={"xs": 12, "md": 12, "lg": 4}),
        ],
        spacing=SPACE_4,
    )

    return ft.Column([urgency, cards, charts], spacing=SPACE_5, expand=True)
