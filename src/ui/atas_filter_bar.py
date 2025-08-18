import asyncio
from typing import Callable, Dict, List, Optional

import flet as ft

from theme.tokens import TOKENS as T
from theme import colors as C
from components import PrimaryButton, SecondaryButton

S, SH, R = T.spacing, T.shadows, T.radius

# Secondary button style shared by filter and sort triggers
SECONDARY_BUTTON_STYLE = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=R.RADIUS_XL),
    padding=ft.padding.symmetric(horizontal=S.SPACE_4, vertical=S.SPACE_2),
    bgcolor={
        ft.MaterialState.DEFAULT: C.SURFACE,
        ft.MaterialState.HOVERED: C.BG_APP,
        ft.MaterialState.PRESSED: C.SURFACE,
        ft.MaterialState.FOCUSED: C.SURFACE,
    },
    side={
        ft.MaterialState.DEFAULT: ft.BorderSide(1, C.BORDER),
        ft.MaterialState.HOVERED: ft.BorderSide(1, C.PRIMARY),
        ft.MaterialState.FOCUSED: ft.BorderSide(2, C.FOCUS_RING),
    },
    color={
        ft.MaterialState.DEFAULT: C.TEXT_PRIMARY,
        ft.MaterialState.HOVERED: C.TEXT_PRIMARY,
        ft.MaterialState.DISABLED: C.TEXT_SECONDARY,
    },
)


def FilterTriggerButton(active_count: int, on_click):
    label = f"Filtrar ({active_count})" if active_count else "Filtrar"
    return ft.OutlinedButton(
        height=40,
        style=SECONDARY_BUTTON_STYLE,
        content=ft.Row(
            [ft.Icon(ft.icons.FILTER_ALT, size=18), ft.Text(label, weight=ft.FontWeight.W_500)],
            spacing=S.SPACE_2,
            tight=True,
        ),
        on_click=on_click,
    )


def SortTriggerButton(current_label: str | None, on_click):
    text = f"Ordenar: {current_label}" if current_label else "Ordenar"
    return ft.OutlinedButton(
        height=40,
        style=SECONDARY_BUTTON_STYLE,
        content=ft.Row(
            [ft.Icon(ft.icons.SORT, size=18), ft.Text(text, weight=ft.FontWeight.W_500)],
            spacing=S.SPACE_2,
            tight=True,
        ),
        on_click=on_click,
    )


def recalc_todas(filters: Dict[str, bool]) -> bool:
    """Return True if all specific filters are active."""
    return all(filters.get(k, False) for k in ("vigente", "a_vencer", "vencida"))


def count_specific(filters: Dict[str, bool]) -> int:
    """Count active specific filters (excluding 'todas')."""
    return sum(1 for k in ("vigente", "a_vencer", "vencida") if filters.get(k, False))


def specific_active(filters: Dict[str, bool]) -> List[str]:
    """Return list of active specific filters."""
    return [k for k in ("vigente", "a_vencer", "vencida") if filters.get(k, False)]


class AtasFilterBar(ft.UserControl):
    """Responsive filter/search/sort bar for Atas screen."""

    def __init__(
        self,
        *,
        on_search_change: Callable[[str], None],
        on_filters_change: Callable[[List[str]], None],
        on_sort_change: Callable[[str], None],
        search: str = "",
        filters: Optional[List[str]] = None,
        sort: str = "mais_recente",
    ) -> None:
        super().__init__()
        self.on_search_change_cb = on_search_change
        self.on_filters_change_cb = on_filters_change
        self.on_sort_change_cb = on_sort_change
        # state holds search text, checkbox states and current sort option
        self.state: Dict[str, any] = {
            "search": search,
            "filters": {
                "todas": False,
                "vigente": False,
                "a_vencer": False,
                "vencida": False,
            },
            "sort": sort,
        }
        if filters:
            for f in filters:
                if f in self.state["filters"]:
                    self.state["filters"][f] = True
        self.state["filters"]["todas"] = recalc_todas(self.state["filters"])
        self._search_task: Optional[asyncio.Task] = None
        self.filter_label_text: Optional[ft.Text] = None
        self.sort_label_text: Optional[ft.Text] = None

    # ------------------------------------------------------------------
    # Build helpers
    # ------------------------------------------------------------------
    def build(self) -> ft.Control:
        self.search_field = ft.TextField(
            value=self.state["search"],
            hint_text="Buscar atas...",
            prefix_icon=ft.icons.SEARCH,
            on_change=self._on_search_change,
            bgcolor="#F3F4F6",
            border_radius=T.radius.RADIUS_LG,
            border_color=C.BORDER,
            focused_border_color=C.PRIMARY,
            content_padding=ft.padding.symmetric(horizontal=S.SPACE_4, vertical=0),
            expand=True,
        )

        self.filter_button = self._build_filter_menu_button()
        self.sort_button = self._build_sort_menu_button()

        buttons_row = ft.Row(
            [self.filter_button, self.sort_button],
            spacing=S.SPACE_3,
        )

        search_container = ft.Container(
            self.search_field,
            col={"xs": 12, "md": 8, "lg": 8},
        )
        buttons_container = ft.Container(
            buttons_row,
            alignment=ft.alignment.center_right,
            col={"xs": 12, "md": 4, "lg": 4},
        )

        row = ft.ResponsiveRow(
            [search_container, buttons_container],
            columns=12,
            spacing=S.SPACE_4,
            run_spacing=S.SPACE_4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        card = ft.Container(
            content=row,
            bgcolor=C.SURFACE,
            border=ft.border.all(1, C.BORDER),
            border_radius=T.radius.RADIUS_LG,
            shadow=SH.SHADOW_SM,
            padding=S.SPACE_4,
            expand=True,
        )

        return card

    # ------------------------------------------------------------------
    # UI builders
    # ------------------------------------------------------------------
    def _build_filter_menu_button(self) -> ft.PopupMenuButton:
        self.cb_todas = ft.Checkbox(
            label="Todas",
            value=self.state["filters"]["todas"],
            on_change=lambda e: self._toggle_todas(e.control.value),
        )
        self.cb_vigente = ft.Checkbox(
            label="Vigentes",
            value=self.state["filters"]["vigente"],
            on_change=lambda e: self._toggle_specific("vigente", e.control.value),
        )
        self.cb_a_vencer = ft.Checkbox(
            label="A Vencer",
            value=self.state["filters"]["a_vencer"],
            on_change=lambda e: self._toggle_specific("a_vencer", e.control.value),
        )
        self.cb_vencida = ft.Checkbox(
            label="Vencidas",
            value=self.state["filters"]["vencida"],
            on_change=lambda e: self._toggle_specific("vencida", e.control.value),
        )

        footer = ft.Row(
            [
                SecondaryButton("Limpar", on_click=self._on_filter_clear, size="sm"),
                PrimaryButton("Aplicar", on_click=self._on_filter_apply, size="sm"),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=S.SPACE_3,
        )

        column = ft.Column(
            [
                self.cb_todas,
                self.cb_vigente,
                self.cb_a_vencer,
                self.cb_vencida,
                footer,
            ],
            spacing=S.SPACE_2,
            tight=True,
            width=300,
        )
        container = ft.Container(
            column,
            padding=S.SPACE_3,
            bgcolor=C.SURFACE,
            border=ft.border.all(1, C.BORDER),
            border_radius=T.radius.RADIUS_LG,
            shadow=SH.SHADOW_MD,
        )

        popup = ft.PopupMenuButton(items=[ft.PopupMenuItem(content=container)])

        def open_menu(e: ft.ControlEvent) -> None:
            popup.open = True
            popup.update()

        trigger = FilterTriggerButton(count_specific(self.state["filters"]), open_menu)
        self.filter_label_text = trigger.content.controls[1]
        popup.content = trigger
        return popup

    def _build_sort_menu_button(self) -> ft.PopupMenuButton:
        self.sort_options = {
            "mais_recente": "Mais recentes",
            "mais_antiga": "Mais antigas",
            "valor_maior": "Maior valor",
            "valor_menor": "Menor valor",
        }
        popup = ft.PopupMenuButton(items=self._build_sort_menu_items())

        def open_menu(e: ft.ControlEvent) -> None:
            popup.open = True
            popup.update()

        current_label = self.sort_options.get(self.state["sort"])
        trigger = SortTriggerButton(current_label, open_menu)
        self.sort_label_text = trigger.content.controls[1]
        popup.content = trigger
        return popup

    def _build_sort_menu_items(self) -> List[ft.PopupMenuItem]:
        items: List[ft.PopupMenuItem] = []
        for key, label in self.sort_options.items():
            checked = self.state["sort"] == key
            icon = ft.Icon(ft.icons.CHECK, size=16) if checked else ft.Container(width=16)
            row = ft.Row([ft.Text(label), ft.Container(expand=True), icon])
            items.append(
                ft.PopupMenuItem(
                    content=row,
                    on_click=lambda e, k=key: self._on_sort_select(k),
                )
            )
        return items

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_search_change(self, e: ft.ControlEvent) -> None:
        query = e.control.value
        self.state["search"] = query
        if self._search_task:
            self._search_task.cancel()
        async def debounce():
            try:
                await asyncio.sleep(0.3)
                if self.on_search_change_cb:
                    self.on_search_change_cb(query)
            except asyncio.CancelledError:
                pass
        self._search_task = asyncio.create_task(debounce())

    def _toggle_todas(self, value: bool) -> None:
        self.state["filters"]["todas"] = value
        for k in ("vigente", "a_vencer", "vencida"):
            self.state["filters"][k] = value
        self._sync_checkboxes()
        self._update_filter_label()

    def _toggle_specific(self, key: str, value: bool) -> None:
        self.state["filters"][key] = value
        self.state["filters"]["todas"] = recalc_todas(self.state["filters"])
        self._sync_checkboxes()
        self._update_filter_label()

    def _sync_checkboxes(self) -> None:
        self.cb_todas.value = self.state["filters"]["todas"]
        self.cb_vigente.value = self.state["filters"]["vigente"]
        self.cb_a_vencer.value = self.state["filters"]["a_vencer"]
        self.cb_vencida.value = self.state["filters"]["vencida"]
        for cb in (self.cb_todas, self.cb_vigente, self.cb_a_vencer, self.cb_vencida):
            cb.update()

    def _filter_label(self) -> str:
        n = count_specific(self.state["filters"])
        return f"Filtrar ({n})" if n else "Filtrar"

    def _update_filter_label(self) -> None:
        if self.filter_label_text:
            self.filter_label_text.value = self._filter_label()
            self.filter_label_text.update()
        self.filter_button.update()

    def _on_filter_clear(self, e: ft.ControlEvent) -> None:
        for k in ("todas", "vigente", "a_vencer", "vencida"):
            self.state["filters"][k] = False
        self._sync_checkboxes()
        self._update_filter_label()
        if self.on_filters_change_cb:
            self.on_filters_change_cb([])

    def _on_filter_apply(self, e: ft.ControlEvent) -> None:
        active = specific_active(self.state["filters"])
        self.filter_button.open = False
        if self.filter_label_text:
            self.filter_label_text.value = self._filter_label()
            self.filter_label_text.update()
        self.filter_button.update()
        if self.on_filters_change_cb:
            self.on_filters_change_cb(active)

    def _on_sort_select(self, key: str) -> None:
        self.state["sort"] = key
        self.sort_button.items = self._build_sort_menu_items()
        if self.sort_label_text:
            self.sort_label_text.value = self._sort_label()
            self.sort_label_text.update()
        self.sort_button.open = False
        self.sort_button.update()
        if self.on_sort_change_cb:
            self.on_sort_change_cb(key)

    def _sort_label(self) -> str:
        label = self.sort_options.get(self.state["sort"], "")
        return "Ordenar" if not label else f"Ordenar: {label}"
