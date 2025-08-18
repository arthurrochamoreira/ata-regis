from typing import Tuple

from theme import colors

# Mapping from status string to (text_color, background_color)
_STATUS_COLORS: dict[str, Tuple[str, str]] = {
    "vigente": (colors.GREEN_DARK, colors.GREEN_BG),
    "a_vencer": (colors.YELLOW_DARK, colors.YELLOW_BG),
    "vencida": (colors.RED_DARK, colors.RED_BG),
}


def get_status_colors(status: str) -> Tuple[str, str]:
    """Return text and background colors for a given status."""
    return _STATUS_COLORS.get(status, (colors.TEXT_PRIMARY, colors.GREY_LIGHT))
