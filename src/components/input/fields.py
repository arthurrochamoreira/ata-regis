"""Input field components."""

from typing import Callable, Optional, Any
import flet as ft

from theme.tokens import TOKENS as T
from . import style

S = T.spacing


def TextInput(
    label: Optional[str] = None,
    *,
    on_change: Optional[Callable[[ft.ControlEvent], None]] = None,
    **kwargs: Any,
) -> ft.TextField:
    """Text input field with shared styling."""
    merged_kwargs = {**style.field_style(), **kwargs}
    return ft.TextField(
        label=label,
        on_change=on_change,
        content_padding=ft.padding.symmetric(horizontal=S.SPACE_3, vertical=S.SPACE_2),
        **merged_kwargs,
    )


def SelectInput(
    options: list[ft.dropdown.Option],
    *,
    on_change: Optional[Callable[[ft.ControlEvent], None]] = None,
    label: Optional[str] = None,
    **kwargs: Any,
) -> ft.Dropdown:
    """Dropdown select input."""
    merged_kwargs = {**style.field_style(), **kwargs}
    return ft.Dropdown(
        options=options,
        on_change=on_change,
        label=label,
        content_padding=ft.padding.symmetric(horizontal=S.SPACE_3, vertical=S.SPACE_2),
        **merged_kwargs,
    )
