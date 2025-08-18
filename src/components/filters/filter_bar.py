"""Filter bar component used on listings."""

from __future__ import annotations

from typing import Callable

import flet as ft

from theme.tokens import TOKENS as T
from theme import colors as C
from ..input import TextInput, SelectInput


class FilterBar(ft.Container):
    """Container grouping search, sort and clear actions."""

    def __init__(
        self,
        on_search: Callable[[str], None],
        on_clear: Callable[[], None],
        on_sort_change: Callable[[str], None],
    ) -> None:
        self._on_search = on_search
        self._on_clear = on_clear
        self._on_sort_change = on_sort_change

        self.search_field = TextInput(
            hint_text="Buscar...",
            expand=True,
            on_change=self._handle_search,
        )
        self.sort_select = SelectInput(
            options=[
                ft.dropdown.Option(key="recentes", text="Mais Recentes"),
                ft.dropdown.Option(key="antigas", text="Mais Antigas"),
            ],
            value="recentes",
            on_change=self._handle_sort,
            width=160,
        )
        clear_btn = ft.IconButton(
            icon=ft.icons.CLEAR,
            icon_color=C.TEXT_PRIMARY,
            tooltip="Limpar",
            on_click=self._handle_clear,
        )
        row = ft.Row(
            [self.search_field, self.sort_select, clear_btn],
            spacing=T.spacing.SPACE_3,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(
            content=row,
            padding=ft.padding.symmetric(horizontal=T.spacing.SPACE_5, vertical=T.spacing.SPACE_5),
        )

    def _handle_search(self, e: ft.ControlEvent) -> None:
        self._on_search(e.control.value)

    def _handle_clear(self, e: ft.ControlEvent) -> None:
        self.search_field.value = ""
        self._on_clear()
        if self.page:
            self.search_field.update()

    def _handle_sort(self, e: ft.ControlEvent) -> None:
        self._on_sort_change(e.control.value)


__all__ = ["FilterBar"]
