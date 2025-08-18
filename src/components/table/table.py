"""Table component built with flet.DataTable."""

from __future__ import annotations

from typing import List, Optional, Callable

import flet as ft

from theme.tokens import TOKENS as T
from ..button import IconAction  # noqa: F401 imported for usage examples

C, S, R, SH, M, TY = (
    T.colors,
    T.spacing,
    T.radius,
    T.shadows,
    T.motion,
    T.typography,
)


def _header_cells(labels: List[str]) -> List[ft.DataColumn]:
    style = ft.TextStyle(
        size=TY.SMALL["size"],
        weight=ft.FontWeight.W_500,
        color=C.NEUTRAL_700,
        font_family=TY.FONT_FAMILY,
    )
    return [ft.DataColumn(ft.Text(lbl.upper(), style=style)) for lbl in labels]


def _row(cells: List[ft.Control], index: int, on_row_hover: Optional[Callable[[int], None]]) -> ft.DataRow:
    row = ft.DataRow(
        [ft.DataCell(c) for c in cells],
        color={"": C.SURFACE, "hovered": C.NEUTRAL_50},
    )
    if on_row_hover:
        row.on_hover = lambda e: on_row_hover(index)
    return row


def Table(
    headers: List[str],
    rows: List[List[ft.Control]],
    *,
    dense: bool = False,
    on_row_hover: Optional[Callable[[int], None]] = None,
) -> ft.DataTable:
    """Create a styled data table."""

    table_rows = [_row(r, i, on_row_hover) for i, r in enumerate(rows)]
    return ft.DataTable(
        columns=_header_cells(headers),
        rows=table_rows,
        heading_row_color=C.NEUTRAL_50,
        horizontal_lines=ft.border.BorderSide(1, C.BORDER_SUBTLE),
        divider_thickness=0,
    )


# Example usage:
# table = Table(["Nome", "Ações"], [[ft.Text("Item"), IconAction(ft.icons.EDIT)]])
