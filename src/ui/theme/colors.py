import flet as ft
from dataclasses import dataclass


@dataclass
class ThemeColors:
    """Collection of colors used by the application.

    This groups the main colors so we can easily switch between
    light and dark modes.  Only the colors that are currently used by
    the layout were added.  More colors can be included when needed.
    """

    background: str
    text: str
    sidebar_bg: str
    sidebar_title: str
    sidebar_link: str
    sidebar_link_hover_bg: str
    sidebar_link_hover_text: str
    sidebar_link_active_bg: str
    sidebar_link_active_text: str
    toggle_bg: str
    toggle_icon: str
    header_bg: str
    header_text: str
    search_bg: str
    search_text: str
    search_placeholder: str
    tabs_border: str
    tab_text: str
    tab_text_hover: str
    tab_active_text: str
    tab_active_border: str


def _light_colors() -> ThemeColors:
    return ThemeColors(
        background=ft.colors.GREY_100,
        text=ft.colors.GREY_900,
        sidebar_bg=ft.colors.WHITE,
        sidebar_title=ft.colors.INDIGO_500,
        sidebar_link=ft.colors.GREY_700,
        sidebar_link_hover_bg=ft.colors.INDIGO_100,
        sidebar_link_hover_text=ft.colors.INDIGO_600,
        sidebar_link_active_bg=ft.colors.INDIGO_50,
        sidebar_link_active_text=ft.colors.INDIGO_600,
        toggle_bg=ft.colors.GREY_100,
        toggle_icon=ft.colors.AMBER_400,
        header_bg=ft.colors.WHITE,
        header_text=ft.colors.GREY_900,
        search_bg=ft.colors.GREY_100,
        search_text=ft.colors.GREY_900,
        search_placeholder=ft.colors.GREY_900,
        tabs_border=ft.colors.GREY_200,
        tab_text=ft.colors.GREY_500,
        tab_text_hover=ft.colors.GREY_700,
        tab_active_text=ft.colors.INDIGO_600,
        tab_active_border=ft.colors.INDIGO_500,
    )


def _dark_colors() -> ThemeColors:
    return ThemeColors(
        background=ft.colors.GREY_900,
        text=ft.colors.WHITE,
        sidebar_bg=ft.colors.GREY_800,
        sidebar_title=ft.colors.INDIGO_500,
        sidebar_link=ft.colors.GREY_300,
        sidebar_link_hover_bg=ft.colors.INDIGO_900,
        sidebar_link_hover_text=ft.colors.INDIGO_300,
        sidebar_link_active_bg=ft.colors.INDIGO_900,
        sidebar_link_active_text=ft.colors.INDIGO_300,
        toggle_bg=ft.colors.GREY_700,
        toggle_icon=ft.colors.GREY_500,
        header_bg=ft.colors.GREY_800,
        header_text=ft.colors.WHITE,
        search_bg=ft.colors.GREY_700,
        search_text=ft.colors.WHITE,
        search_placeholder=ft.colors.WHITE,
        tabs_border=ft.colors.GREY_700,
        tab_text=ft.colors.GREY_400,
        tab_text_hover=ft.colors.GREY_200,
        tab_active_text=ft.colors.INDIGO_400,
        tab_active_border=ft.colors.INDIGO_500,
    )


LIGHT_COLORS = _light_colors()
DARK_COLORS = _dark_colors()


def get_theme(mode: ft.ThemeMode) -> ThemeColors:
    """Return colors for the given ``mode``."""

    return LIGHT_COLORS if mode == ft.ThemeMode.LIGHT else DARK_COLORS
