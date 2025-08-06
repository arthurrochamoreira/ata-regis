from typing import Tuple

from ui.theme import colors

# Mapping from status string to (text_color, background_color)
_STATUS_COLORS: dict[str, Tuple[str, str]] = {
    "vigente": (colors.BADGE_VIGENTE_TEXT, colors.BADGE_VIGENTE_BG),
    "a_vencer": (colors.BADGE_A_VENCER_TEXT, colors.BADGE_A_VENCER_BG),
    "vencida": (colors.BADGE_VENCIDA_TEXT, colors.BADGE_VENCIDA_BG),
}


def get_status_colors(status: str) -> Tuple[str, str]:
    """Return text and background colors for a given status."""
    return _STATUS_COLORS.get(status, (colors.APP_TEXT, colors.TABLE_DIVIDER))
