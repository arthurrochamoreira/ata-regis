import flet as ft

# Default font family used across the application
FONT_FAMILY = "Inter"
# Backwards compatibility
FONT_SANS = FONT_FAMILY

# ---------------------------------------------------------------------------
# Typography scale
# ---------------------------------------------------------------------------
# Diretrizes de uso:
# - H1/H2/H3: títulos e seções
# - BODY: texto corrido
# - SMALL: legendas e observações
H1 = {"size": 30, "weight": ft.FontWeight.W_600, "line_height": 1.25}
H2 = {"size": 24, "weight": ft.FontWeight.W_600, "line_height": 1.25}
H3 = {"size": 20, "weight": ft.FontWeight.W_600, "line_height": 1.25}
BODY = {"size": 14, "weight": ft.FontWeight.NORMAL, "line_height": 1.5}
SMALL = {"size": 12, "weight": ft.FontWeight.NORMAL, "line_height": 1.5}

# Legacy size tokens preserved for compatibility
TEXT_XL = 20  # text-xl
TEXT_LG = 18  # text-lg
TEXT_BASE = 16  # base text
TEXT_SM = 14  # text-sm
TEXT_XS = 11  # text-xs

# Font weight tokens
FONT_BOLD = ft.FontWeight.BOLD

# Line height and letter spacing tokens
# Approximation of Tailwind's leading-5 and tracking-wider
LEADING_5 = 1.25
TRACKING_WIDER = 0.05

def text(
    value: str,
    *,
    size: int | float = TEXT_SM,
    weight: ft.FontWeight | None = None,
    line_height: float | None = None,
    letter_spacing: float | None = None,
    color: str | None = None,
    **kwargs,
) -> ft.Text:
    """Create a Text control with the project default font settings."""
    return ft.Text(
        value,
        style=ft.TextStyle(
            font_family=FONT_FAMILY,
            size=size,
            weight=weight,
            height=line_height,
            letter_spacing=letter_spacing,
            color=color,
        ),
        **kwargs,
    )

def text_style(
    *,
    size: int | float = TEXT_SM,
    weight: ft.FontWeight | None = None,
    line_height: float | None = None,
    letter_spacing: float | None = None,
    color: str | None = None,
) -> ft.TextStyle:
    """Return a TextStyle with default font family and given parameters."""
    return ft.TextStyle(
        font_family=FONT_FAMILY,
        size=size,
        weight=weight,
        height=line_height,
        letter_spacing=letter_spacing,
        color=color,
    )
