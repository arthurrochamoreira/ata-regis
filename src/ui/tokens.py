SPACE_1 = 4
SPACE_2 = 8
SPACE_3 = 12
SPACE_4 = 16
SPACE_5 = 24  # padding=24 (Style Guide)
SPACE_6 = 32

import flet as ft

# Global palette (Style Guide)
PRIMARY = ft.colors.INDIGO_600
SUCCESS = ft.colors.GREEN_500
DANGER = ft.colors.RED_500
WARNING = ft.colors.ORANGE_500
TEXT_PRIMARY = ft.colors.GREY_800
TEXT_SECONDARY = ft.colors.GREY_500
SIDEBAR_BG = ft.colors.GREY_800
SIDEBAR_TEXT = ft.colors.GREY_200
GREY_LIGHT = ft.colors.GREY_300
CARD_BG = ft.colors.WHITE
APP_BG = ft.colors.GREY_100

# Card shadow (Style Guide)
CARD_SHADOW = ft.BoxShadow(
    spread_radius=1,
    blur_radius=5,
    color=ft.colors.with_opacity(0.1, "black"),
    offset=ft.Offset(0, 2),
)

# Card shadow hover (Style Guide)
CARD_SHADOW_HOVER = ft.BoxShadow(
    spread_radius=2,
    blur_radius=10,
    color=ft.colors.with_opacity(0.15, "black"),
    offset=ft.Offset(0, 4),
)

def build_card(title: str, icon: ft.Control, content: ft.Control) -> ft.Control:
    """Reusable card following the Style Guide."""
    header = ft.Row(
        [icon, ft.Text(title, size=18, weight=ft.FontWeight.SEMI_BOLD, color=TEXT_PRIMARY)],
        spacing=SPACE_2,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return ft.Container(
        content=ft.Column([header, content], spacing=SPACE_5),
        padding=ft.padding.all(SPACE_5),  # padding=24 (Style Guide)
        border=ft.border.all(1, GREY_LIGHT),
        border_radius=12,  # cards radius=12 (Style Guide)
        bgcolor=CARD_BG,
        shadow=CARD_SHADOW,
    )
