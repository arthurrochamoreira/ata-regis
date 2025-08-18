import asyncio
from typing import Callable, Dict, List, Optional

import flet as ft

from theme.tokens import TOKENS as T
from theme import colors as C
from components import PrimaryButton, SecondaryButton

S, SH = T.spacing, T.shadows


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
        # visibility of dropdowns is controlled via ``ft.Ref`` objects
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

        self.filter_button = SecondaryButton(
            text=self._filter_label(),
            icon=ft.icons.TUNE,
            on_click=self._toggle_filter_menu,
        )
        self.sort_button = SecondaryButton(
            text="Ordenar",
            icon=ft.icons.SORT,
            on_click=self._toggle_sort_menu,
        )

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

        # Refs to control visibility of overlay and dropdown menus
        self.ref_click_out_overlay: ft.Ref[ft.Container] = ft.Ref()
        self.ref_filter_menu: ft.Ref[ft.Container] = ft.Ref()
        self.ref_sort_menu: ft.Ref[ft.Container] = ft.Ref()

        overlay = ft.Container(
            ref=self.ref_click_out_overlay,
            expand=True,
            bgcolor=ft.colors.TRANSPARENT,
            visible=False,
            on_click=lambda e: self._close_menus(),
        )

        filter_dropdown = ft.Container(
            ref=self.ref_filter_menu,
            top=70,
            left=0,
            content=self._build_filter_menu(),
            visible=False,
        )
        sort_dropdown = ft.Container(
            ref=self.ref_sort_menu,
            top=70,
            left=160,
            content=self._build_sort_menu(),
            visible=False,
        )

        return ft.Stack(
            [card, overlay, filter_dropdown, sort_dropdown],
            expand=True,
        )

    # ------------------------------------------------------------------
    # UI builders
    # ------------------------------------------------------------------
    def _build_filter_menu(self) -> ft.Container:
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

        content = ft.Column(
            [self.cb_todas, self.cb_vigente, self.cb_a_vencer, self.cb_vencida, footer],
            spacing=S.SPACE_2,
        )

        return ft.Container(
            content,
            width=300,
            padding=S.SPACE_3,
            bgcolor=C.SURFACE,
            border=ft.border.all(1, C.BORDER),
            border_radius=T.radius.RADIUS_LG,
            shadow=SH.SHADOW_MD,
        )

    def _build_sort_menu(self) -> ft.Container:
        options = [
            ("mais_recente", "Mais recentes"),
            ("mais_antiga", "Mais antigas"),
            ("valor_maior", "Maior valor"),
            ("valor_menor", "Menor valor"),
        ]
        self.sort_buttons: Dict[str, ft.TextButton] = {}
        buttons: List[ft.Control] = []
        for key, label in options:
            btn = ft.TextButton(label, on_click=lambda e, k=key: self._on_sort_select(k))
            self.sort_buttons[key] = btn
            buttons.append(btn)
        self._update_sort_buttons()
        return ft.Container(
            ft.Column(buttons, spacing=S.SPACE_1),
            width=220,
            padding=S.SPACE_3,
            bgcolor=C.SURFACE,
            border=ft.border.all(1, C.BORDER),
            border_radius=T.radius.RADIUS_LG,
            shadow=SH.SHADOW_MD,
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _toggle_filter_menu(self, e: ft.ControlEvent) -> None:
        """Open/close filter dropdown, hiding others."""
        filter_menu = self.ref_filter_menu.current
        overlay = self.ref_click_out_overlay.current
        sort_menu = self.ref_sort_menu.current
        if filter_menu.visible:
            self._close_menus()
            return
        overlay.visible = True
        filter_menu.visible = True
        sort_menu.visible = False
        self.update()

    def _toggle_sort_menu(self, e: ft.ControlEvent) -> None:
        """Open/close sort dropdown, hiding filter dropdown."""
        sort_menu = self.ref_sort_menu.current
        overlay = self.ref_click_out_overlay.current
        filter_menu = self.ref_filter_menu.current
        if sort_menu.visible:
            self._close_menus()
            return
        overlay.visible = True
        sort_menu.visible = True
        filter_menu.visible = False
        self.update()

    def _close_menus(self, e: Optional[ft.ControlEvent] = None) -> None:
        overlay = self.ref_click_out_overlay.current
        filter_menu = self.ref_filter_menu.current
        sort_menu = self.ref_sort_menu.current
        overlay.visible = False
        filter_menu.visible = False
        sort_menu.visible = False
        self.update()

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
        self.filter_button.text = self._filter_label()
        self.filter_button.update()

    def _on_filter_clear(self, e: ft.ControlEvent) -> None:
        for k in ("todas", "vigente", "a_vencer", "vencida"):
            self.state["filters"][k] = False
        self._sync_checkboxes()
        self._update_filter_label()

    def _on_filter_apply(self, e: ft.ControlEvent) -> None:
        active = specific_active(self.state["filters"])
        self._close_menus()
        if self.on_filters_change_cb:
            self.on_filters_change_cb(active)

    def _on_sort_select(self, key: str) -> None:
        self.state["sort"] = key
        self._update_sort_buttons()
        self._close_menus()
        if self.on_sort_change_cb:
            self.on_sort_change_cb(key)

    def _update_sort_buttons(self) -> None:
        for key, btn in self.sort_buttons.items():
            selected = self.state["sort"] == key
            btn.style = ft.ButtonStyle(
                bgcolor={ft.MaterialState.DEFAULT: C.PRIMARY if selected else C.SURFACE},
                color={ft.MaterialState.DEFAULT: ft.colors.WHITE if selected else C.TEXT_PRIMARY},
            )
            # Buttons might be styled before being added to the page.
            # ``Control.update`` requires the control to be attached to a page,
            # so we only call ``update`` when the button is already mounted.
            if btn.page:
                btn.update()
