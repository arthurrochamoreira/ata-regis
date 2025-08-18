from typing import Tuple

from ui.theme import colors

# Mapping from status string to (text_color, background_color)
_STATUS_COLORS: dict[str, Tuple[str, str]] = {
    "vigente": (colors.SEM.success_text, colors.SEM.success_bg),
    "a_vencer": (colors.SEM.warning_text, colors.SEM.warning_bg),
    "vencida": (colors.SEM.error_text, colors.SEM.error_bg),
}


def get_status_colors(status: str) -> Tuple[str, str]:
    """Return text and background colors for a given status."""
    return _STATUS_COLORS.get(status, (colors.SEM.text, colors.SEM.border))
