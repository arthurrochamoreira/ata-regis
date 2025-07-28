SPACE_1 = 4
SPACE_2 = 8
SPACE_3 = 12
SPACE_4 = 16
SPACE_5 = 24
SPACE_6 = 32

import flet as ft

PRIMARY = ft.colors.BLUE
DANGER = ft.colors.RED
SUCCESS = ft.colors.GREEN
WARNING = ft.colors.ORANGE
GREY_LIGHT = ft.colors.GREY_300

def build_card(title: str, icon: ft.Control, content: ft.Control) -> ft.Control:
    header = ft.Row(
        [icon, ft.Text(title, size=16, weight=ft.FontWeight.W_600)],
        spacing=SPACE_2,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=ft.Column([header, content], spacing=SPACE_4),
        padding=SPACE_5,
        border=ft.border.all(1, GREY_LIGHT),
        border_radius=12,
        bgcolor=ft.colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )
