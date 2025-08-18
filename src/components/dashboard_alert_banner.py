import flet as ft
from components.dashboard import AlertBanner


def make_alert_banner(*, **deps):
    count = deps.get("count", 0)
    return AlertBanner(
        icon=ft.icons.WARNING_AMBER_ROUNDED,
        title="Atenção",
        subtitle=f"Você possui {count} ata(s) vencendo em 90 dias ou menos.",
    )
