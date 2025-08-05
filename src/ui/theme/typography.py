import flet as ft

# Default sans-serif font family used across the application
FONT_SANS = "Inter"

# Text size tokens (TailwindCSS equivalents)
TEXT_XL = 20  # text-xl
TEXT_SM = 14  # text-sm

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
            font_family=FONT_SANS,
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
        font_family=FONT_SANS,
        size=size,
        weight=weight,
        height=line_height,
        letter_spacing=letter_spacing,
        color=color,
    )
