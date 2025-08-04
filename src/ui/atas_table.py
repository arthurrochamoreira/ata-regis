import flet as ft
from typing import Any, Callable, List, Optional


class AtasTable(ft.UserControl):
    """Reusable table component for Ata listings with centralized style."""

    def __init__(
        self,
        columns: List[str],
        rows: List[Any],
        on_view: Optional[Callable[[Any], None]] = None,
        on_edit: Optional[Callable[[Any], None]] = None,
        on_delete: Optional[Callable[[Any], None]] = None,
        *,
        page_width: float = 1000.0,
    ) -> None:
        super().__init__()
        self.columns = columns
        self.rows = rows
        self.on_view = on_view
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.page_width = page_width

    # ------------------------------------------------------------------
    def build(self) -> ft.Control:  # pragma: no cover - UI code
        font_size = 12 if self.page_width < 768 else 14

        data_columns: List[ft.DataColumn] = []
        for col in self.columns:
            expand = 2 if col.upper() in ("OBJETO", "FORNECEDOR") else 1
            data_columns.append(
                ft.DataColumn(
                    label=ft.Container(
                            ft.Text(
                                col.upper(),
                                text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_600,
                                size=font_size,
                            ),
                        alignment=ft.alignment.center,
                        expand=expand,
                    )
                )
            )

        if any([self.on_view, self.on_edit, self.on_delete]):
            data_columns.append(
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text(
                            "AÇÕES",
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_600,
                            size=font_size,
                        ),
                        alignment=ft.alignment.center,
                        expand=1,
                    )
                )
            )

        data_rows: List[ft.DataRow] = []
        for row in self.rows:
            if isinstance(row, dict):
                values = row.get("values", [])
                data = row.get("data", row.get("values"))
            else:
                values = row
                data = row

            cells: List[ft.DataCell] = []
            for col, value in zip(self.columns, values):
                expand = 2 if col.upper() in ("OBJETO", "FORNECEDOR") else 1
                if isinstance(value, ft.Control):
                    cell_content = value
                else:
                    cell_content = ft.Text(
                        str(value),
                        text_align=ft.TextAlign.CENTER,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        size=font_size,
                    )
                cells.append(
                    ft.DataCell(
                        ft.Container(
                            cell_content,
                            alignment=ft.alignment.center,
                            expand=expand,
                        )
                    )
                )

            if any([self.on_view, self.on_edit, self.on_delete]):
                icons: List[ft.Control] = []
                if self.on_view:
                    icons.append(
                        ft.IconButton(
                            icon=ft.icons.VISIBILITY,
                            tooltip="Visualizar",
                            on_click=lambda e, d=data: self.on_view(d),
                            adaptive=True,
                            style=ft.ButtonStyle(
                                color={
                                    ft.MaterialState.HOVERED: ft.colors.INDIGO_600,
                                    "": ft.colors.GREY_700,
                                }
                            ),
                        )
                    )
                if self.on_edit:
                    icons.append(
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            tooltip="Editar",
                            on_click=lambda e, d=data: self.on_edit(d),
                            adaptive=True,
                            style=ft.ButtonStyle(
                                color={
                                    ft.MaterialState.HOVERED: ft.colors.INDIGO_600,
                                    "": ft.colors.GREY_700,
                                }
                            ),
                        )
                    )
                if self.on_delete:
                    icons.append(
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Excluir",
                            on_click=lambda e, d=data: self.on_delete(d),
                            adaptive=True,
                            style=ft.ButtonStyle(
                                color={
                                    ft.MaterialState.HOVERED: ft.colors.INDIGO_600,
                                    "": ft.colors.GREY_700,
                                }
                            ),
                        )
                    )
                action_row = ft.Row(
                    icons, alignment=ft.MainAxisAlignment.CENTER, spacing=4
                )
                cells.append(
                    ft.DataCell(
                        ft.Container(
                            action_row,
                            alignment=ft.alignment.center,
                            expand=1,
                        )
                    )
                )

            data_rows.append(ft.DataRow(cells=cells))

        table = ft.DataTable(
            columns=data_columns,
            rows=data_rows,
            data_row_min_height=48,
            heading_row_height=48,
            column_spacing=0,
            horizontal_margin=16,
            vertical_lines=ft.BorderSide(0, "transparent"),
            heading_row_color=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_100),
            data_row_color={
                ft.MaterialState.HOVERED: ft.colors.GREY_100,
                "": ft.colors.WHITE,
            },
        )
        return table
