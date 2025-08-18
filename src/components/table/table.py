"""Table components built on top of flet.DataTable."""

from typing import List
import flet as ft

from theme.tokens import TOKENS as T
from theme import colors as C

S = T.spacing


def TableHeader(labels: List[str]) -> List[ft.DataColumn]:
    """Create data table header columns."""
    return [ft.DataColumn(ft.Text(lbl, color=C.TEXT_SECONDARY)) for lbl in labels]


def TableRow(cells: List[ft.Control]) -> ft.DataRow:
    """Create a table row from controls."""
    return ft.DataRow([ft.DataCell(cell) for cell in cells])


def TableCell(content: ft.Control) -> ft.DataCell:
    """Wrap a control into a data cell."""
    return ft.DataCell(content)


def Table(columns: List[str], rows: List[List[ft.Control]]) -> ft.DataTable:
    """Convenience wrapper to create a table."""
    return ft.DataTable(
        columns=TableHeader(columns),
        rows=[TableRow(r) for r in rows],
        heading_row_color=C.BG_APP,
        horizontal_lines=ft.border.BorderSide(1, C.BORDER),
        data_row_height=56,
        divider_thickness=0,
    )
