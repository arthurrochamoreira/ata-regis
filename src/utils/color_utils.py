from typing import Tuple

from theme import colors as C

# Mapping from status string to (text_color, background_color)
_STATUS_COLORS: dict[str, Tuple[str, str]] = {
    "vigente": (C.SUCCESS_TEXT, C.SUCCESS_BG),
    "a_vencer": (C.WARNING_TEXT, C.WARNING_BG),
    "vencida": (C.ERROR_TEXT, C.ERROR_BG),
}


def get_status_colors(status: str) -> Tuple[str, str]:
    """Return text and background colors for a given status."""
    return _STATUS_COLORS.get(status, (C.TEXT_PRIMARY, C.BG_APP))
