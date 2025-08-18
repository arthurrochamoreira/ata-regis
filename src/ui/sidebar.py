from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Any

import flet as ft

from theme.tokens import TOKENS as T

C, S, R, SH, M = T.colors, T.spacing, T.radius, T.shadows, T.motion

# === Constantes de layout/estilo ===

SelectCallback = Callable[[str], None]
ClickCallback = Callable[[ft.ControlEvent], None]


@dataclass(frozen=True)
class SidebarItemData:
    """Estrutura de dados esperada para cada item da Sidebar."""
    id: str
    label: str
    icon: str                      # ex.: ft.icons.HOME
    badge: Optional[str | int] = None
    selected: bool = False
    on_click: Optional[ClickCallback] = None


def _as_item_data(data: dict[str, Any]) -> SidebarItemData:
    """Converte dict frouxo em SidebarItemData tipado, com validação mínima."""
    try:
        return SidebarItemData(
            id=str(data["id"]),
            label=str(data["label"]),
            icon=str(data["icon"]),
            badge=data.get("badge"),
            selected=bool(data.get("selected", False)),
            on_click=data.get("on_click"),
        )
    except KeyError as exc:
        missing = ", ".join(k for k in ("id", "label", "icon") if k not in data)
        raise KeyError(f"SidebarItem requer chaves: id, label, icon (faltando: {missing})") from exc


def _hover_style(bg_hover: str) -> ft.ButtonStyle:
    """Estilo padrão de botão com hover consistente."""
    return ft.ButtonStyle(
        padding=0,
        shape=ft.RoundedRectangleBorder(radius=0),
        bgcolor={ft.MaterialState.HOVERED: bg_hover},
    )


class SidebarItem(ft.Container):
    """Item de navegação usado dentro de :class:`Sidebar`.

    - No modo expandido, mostra ícone + label (+ badge).
    - No modo colapsado, mostra apenas o ícone centralizado com tooltip.
    - O indicador à esquerda é overlay (não desloca o conteúdo).
    """

    def __init__(
        self,
        raw_data: dict,
        *,
        collapsed: bool,
        on_select: SelectCallback,
        duration: int,
        curve: str,
    ) -> None:
        super().__init__(padding=0)

        self._data: SidebarItemData = _as_item_data(raw_data)
        self._on_select: SelectCallback = on_select
        self._external_click: Optional[ClickCallback] = self._data.on_click
        self._hover_bg = C.GREY_LIGHT

        # --- ÍCONES (instâncias separadas para evitar múltiplos pais) ---
        self._icon_expanded = ft.Icon(self._data.icon, size=T.sizes.ICON_MD, color=C.TEXT_PRIMARY)
        self._icon_collapsed = ft.Icon(self._data.icon, size=T.sizes.ICON_MD, color=C.TEXT_PRIMARY)
        self._icons = (self._icon_expanded, self._icon_collapsed)  # para updates em lote

        # Slots fixos para ambos os modos
        self._icon_slot_expanded = ft.Container(
            content=self._icon_expanded,
            width=T.sizes.WIDTH_SIDEBAR_COLLAPSED,
            height=T.sizes.ITEM_TOUCH,
            alignment=ft.alignment.center,
        )
        self._icon_slot_collapsed = ft.Container(
            content=self._icon_collapsed,
            width=T.sizes.WIDTH_SIDEBAR_COLLAPSED,
            height=T.sizes.ITEM_TOUCH,
            alignment=ft.alignment.center,
        )

        # Label e (opcional) badge
        self._label = ft.Text(self._data.label, color=C.TEXT_PRIMARY)
        row_controls: List[ft.Control] = [self._icon_slot_expanded, self._label]

        self._badge: Optional[ft.Control] = None
        if self._data.badge is not None:
            self._badge = ft.Container(
                content=ft.Text(str(self._data.badge)),
                padding=ft.padding.symmetric(horizontal=S.SPACE_2, vertical=S.SPACE_1),
                border_radius=R.RADIUS_MD,
                bgcolor=C.INDIGO_BG,
                alignment=ft.alignment.center,
                visible=not collapsed,
            )
            row_controls.append(self._badge)

        # Botão (expandido): ícone + label (+ badge)
        self._row_btn = ft.TextButton(
            content=ft.Row(
                row_controls,
                spacing=S.SPACE_3,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=T.sizes.WIDTH_SIDEBAR_OPEN,
            height=T.sizes.ITEM_TOUCH,
            on_click=self._handle_click,
            style=_hover_style(self._hover_bg),
        )
        self._row_btn.style.padding = ft.padding.only(left=0, right=S.SPACE_3)
        self._row_btn.aria_label = self._data.label

        # Botão (colapsado): apenas o ícone centralizado
        self._icon_btn = ft.TextButton(
            content=self._icon_slot_collapsed,
            width=T.sizes.WIDTH_SIDEBAR_COLLAPSED,
            height=T.sizes.ITEM_TOUCH,
            tooltip=self._data.label if collapsed else None,
            on_click=self._handle_click,
            style=_hover_style(self._hover_bg),
        )
        self._icon_btn.aria_label = self._data.label

        # Wrapper (colapsado) – mantém área clicável centralizada
        self._icon_wrapper = ft.Container(
            content=self._icon_btn,
            width=T.sizes.WIDTH_SIDEBAR_COLLAPSED,
            height=T.sizes.ITEM_TOUCH,
            alignment=ft.alignment.center,
        )

        # Caixa de conteúdo principal (sem borda)
        self._content_box = ft.Container(
            content=self._icon_wrapper if collapsed else self._row_btn,
            width=T.sizes.WIDTH_SIDEBAR_COLLAPSED if collapsed else T.sizes.WIDTH_SIDEBAR_OPEN,
            height=T.sizes.ITEM_TOUCH,
            alignment=ft.alignment.center,
            bgcolor=None,  # aplicado quando selecionado
        )

        # Indicador overlay (sem usar ft.Positioned)
        self._indicator = ft.Container(
            width=T.sizes.INDICATOR_W,
            height=T.sizes.ITEM_TOUCH,
            bgcolor=C.TRANSPARENT,
        )
        # Ancoragem absoluta no Stack
        self._indicator.left = 0
        self._indicator.top = 0
        self._indicator.bottom = 0

        # Stack: conteúdo (fundo) + indicador (sobreposto à esquerda)
        self._item_box = ft.Stack(
            controls=[
                self._content_box,   # 1º: conteúdo
                self._indicator,     # 2º: indicador overlay (fica por cima)
            ],
            width=self._content_box.width,
            height=T.sizes.ITEM_TOUCH,
        )

        # Container raiz
        self.width = self._item_box.width
        self.height = T.sizes.ITEM_TOUCH
        self.alignment = ft.alignment.center
        self.content = self._item_box

        # Estado inicial de seleção
        self.set_selected(self._data.selected)

    # --- Handlers / Updates de estado -------------------------------------------------

    def _handle_click(self, e: ft.ControlEvent) -> None:
        if self._external_click:
            self._external_click(e)
        self._on_select(self._data.id)

    def set_collapsed(self, collapsed: bool) -> None:
        """Aplica layout do modo colapsado/expandido e atualiza visibilidades."""
        self._content_box.content = self._icon_wrapper if collapsed else self._row_btn
        self._content_box.width = T.sizes.WIDTH_SIDEBAR_COLLAPSED if collapsed else T.sizes.WIDTH_SIDEBAR_OPEN
        self._item_box.width = self._content_box.width
        self.width = self._item_box.width

        self._icon_btn.tooltip = self._data.label if collapsed else None
        if self._badge:
            self._badge.visible = not collapsed

        self.update()

    def set_selected(self, selected: bool) -> None:
        """Atualiza o visual de item ativo (indicador e cores)."""
        active_color = C.INDIGO
        active_bg = C.INDIGO_BG

        # Indicador overlay e fundo suave
        self._indicator.bgcolor = active_color if selected else C.TRANSPARENT
        self._content_box.bgcolor = active_bg if selected else None

        # Texto e ícones
        self._label.weight = ft.FontWeight.W_600 if selected else ft.FontWeight.NORMAL
        self._label.color = active_color if selected else C.TEXT_PRIMARY
        for icon in self._icons:
            icon.color = active_color if selected else C.TEXT_PRIMARY

        if self.page:
            self.update()


class Sidebar(ft.Container):
    """Sidebar de navegação expansível/colapsável com persistência de estado."""

    def __init__(
        self,
        page: ft.Page,
        items: List[dict],
        *,
        collapsed: Optional[bool] = None,
        on_toggle: Optional[Callable[[bool], None]] = None,
        open_width: int = T.sizes.WIDTH_SIDEBAR_OPEN,
        closed_width: int = T.sizes.WIDTH_SIDEBAR_COLLAPSED,  # travado para usar a coluna de ícones
        duration: int = M.DURATION_SIDEBAR,
        curve: str = "ease",
    ) -> None:
        self.page = page
        self.on_toggle = on_toggle
        self.open_width = max(open_width, T.sizes.WIDTH_SIDEBAR_OPEN)
        self.closed_width = closed_width
        self.duration = duration
        self.curve = curve

        # Estado inicial (persistido)
        stored = self.page.client_storage.get("sidebar_collapsed")
        if collapsed is None:
            collapsed = json.loads(stored) if stored is not None else False
        self.collapsed = collapsed

        # Itens
        self._items: List[SidebarItem] = [
            SidebarItem(
                raw_data=d,
                collapsed=self.collapsed,
                on_select=self._on_item_selected,
                duration=duration,
                curve=curve,
            )
            for d in items
        ]

        # Botão de Toggle (mesmo slot da coluna de ícones)
        self._menu_icon = ft.Icon(ft.icons.MENU, size=T.sizes.ICON_MD, color=C.TEXT_PRIMARY)
        self._menu_icon.rotate = ft.transform.Rotate(0 if not self.collapsed else math.pi)
        self._menu_icon.animate_rotation = ft.animation.Animation(duration, curve)

        self.toggle_btn = ft.TextButton(
            content=ft.Container(
                content=self._menu_icon,
                width=self.closed_width,
                height=T.sizes.ITEM_TOUCH,
                alignment=ft.alignment.center,
            ),
            width=self.closed_width,
            height=T.sizes.ITEM_TOUCH,
            tooltip=self._toggle_tooltip(self.collapsed),
            on_click=self.toggle_sidebar,
            style=_hover_style(C.GREY_LIGHT),
        )
        self.toggle_btn.aria_label = self._toggle_tooltip(self.collapsed)

        self.toggle_box = ft.Container(
            content=self.toggle_btn,
            width=self.closed_width,
            height=T.sizes.ITEM_TOUCH,
            alignment=ft.alignment.center,
        )

        content = ft.Column(
            [self.toggle_box, *self._items],
            spacing=S.SPACE_2,
            expand=True,
        )

        super().__init__(
            content=content,
            width=self.open_width if not self.collapsed else self.closed_width,
            bgcolor=C.WHITE,
            padding=ft.padding.symmetric(vertical=S.SPACE_5),
            shadow=SH.SHADOW_XL,
            animate=ft.animation.Animation(duration, curve),
        )

    # --- Handlers / API pública -------------------------------------------------------

    def _on_item_selected(self, item_id: str) -> None:
        for item in self._items:
            item.set_selected(item._data.id == item_id)
        self.update()

    def toggle_sidebar(self, e: Optional[ft.ControlEvent] = None) -> None:
        self.set_collapsed(not self.collapsed)

    def set_collapsed(self, value: bool) -> None:
        self.collapsed = value
        self.width = self.open_width if not value else self.closed_width

        self._menu_icon.rotate.angle = 0 if not value else math.pi
        tip = self._toggle_tooltip(value)
        self.toggle_btn.tooltip = tip
        self.toggle_btn.aria_label = tip

        for item in self._items:
            item.set_collapsed(value)

        self.page.client_storage.set("sidebar_collapsed", json.dumps(value))
        if self.on_toggle:
            self.on_toggle(value)
        self.update()

    def update_layout(self, width: int) -> None:
        """Exemplo de responsividade simples: colapsa < 768px."""
        if width < 768 and not self.collapsed:
            self.set_collapsed(True)

    # --- Helpers privados -------------------------------------------------------------

    @staticmethod
    def _toggle_tooltip(collapsed: bool) -> str:
        return "Expandir menu" if collapsed else "Colapsar menu"
