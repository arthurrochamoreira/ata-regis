"""Badge and indicator widgets."""
from flet import colors, Container, padding, Text
from ..constants import SPACE_1, SPACE_3


def status_badge(status: str) -> Container:
    """Return a colored badge for status."""
    bg, fg = {
        "Vigente": (colors.GREEN_100, colors.GREEN_900),
        "À Vencer": (colors.AMBER_100, colors.AMBER_900),
        "Vencida": (colors.RED_100, colors.RED_900),
    }.get(status, (colors.GREY_200, colors.GREY_900))
    return Container(
        bgcolor=bg,
        border_radius=12,
        padding=padding.symmetric(vertical=SPACE_1, horizontal=SPACE_3),
        content=Text(status, size=12, color=fg),
    )
