"""Input field components."""

from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from theme.tokens import TOKENS as T
from . import style

C, S, R, SH, M, TY = (
    T.colors,
    T.spacing,
    T.radius,
    T.shadows,
    T.motion,
    T.typography,
)


def TextInput(
    label: str,
    *,
    hint: Optional[str] = None,
    value: str = "",
    error: Optional[str] = None,
    on_change: Optional[Callable[[ft.ControlEvent], None]] = None,
    password: bool = False,
    prefix_icon: Optional[str] = None,
    suffix_icon: Optional[str] = None,
) -> ft.Column:
    """Text input with label, helper and error support."""

    field = ft.TextField(
        value=value,
        on_change=on_change,
        password=password,
        prefix_icon=prefix_icon,
        suffix_icon=suffix_icon,
        **style.field_style(error=error is not None),
    )

    label_text = ft.Text(
        label,
        size=TY.SMALL["size"],
        weight=ft.FontWeight.W_500,
        color=C.NEUTRAL_600,
    )

    helper_ctrl: ft.Text | None = None
    if error:
        helper_ctrl = ft.Text(
            error,
            size=TY.SMALL["size"],
            color=C.ERROR_TEXT,
        )
    elif hint:
        helper_ctrl = ft.Text(
            hint,
            size=TY.SMALL["size"],
            color=C.NEUTRAL_600,
        )

    controls: list[ft.Control] = [label_text, field]
    if helper_ctrl:
        controls.append(helper_ctrl)
    return ft.Column(controls, spacing=S.SPACE_1)


# Example usage:
# field = TextInput("Nome", hint="Digite seu nome")
