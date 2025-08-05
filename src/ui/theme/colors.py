import flet as ft

LIGHT = {
    "app_bg": ft.colors.GREY_100,
    "text": ft.colors.GREY_900,
    "sidebar": {
        "bg": ft.colors.WHITE,
        "title": ft.colors.INDIGO_500,
        "link": ft.colors.GREY_700,
        "link_hover_bg": ft.colors.INDIGO_100,
        "link_hover_text": ft.colors.INDIGO_600,
        "link_active_bg": ft.colors.INDIGO_50,
        "link_active_text": ft.colors.INDIGO_600,
        "toggle_bg": ft.colors.GREY_100,
        "icon_sun": ft.colors.AMBER_400,
        "icon_moon": ft.colors.GREY_500,
    },
    "header": {
        "bg": ft.colors.WHITE,
        "title": ft.colors.GREY_900,
        "search_bg": ft.colors.GREY_100,
        "search_text": ft.colors.GREY_900,
        "search_placeholder": ft.colors.GREY_900,
        "search_icon": ft.colors.GREY_400,
        "search_focus": ft.colors.INDIGO_500,
        "button_bg": ft.colors.INDIGO_600,
        "button_text": ft.colors.WHITE,
        "button_hover_bg": ft.colors.INDIGO_700,
    },
    "tabs": {
        "border": ft.colors.GREY_200,
        "text": ft.colors.GREY_500,
        "hover": ft.colors.GREY_700,
        "active_border": ft.colors.INDIGO_500,
        "active_text": ft.colors.INDIGO_600,
    },
    "table": {
        "card_bg": ft.colors.WHITE,
        "title_text": ft.colors.GREY_900,
        "header_border": ft.colors.GREY_200,
        "header_bg": ft.colors.GREY_50,
        "header_text": ft.colors.GREY_500,
        "number_text": ft.colors.GREY_900,
        "other_text": ft.colors.GREY_500,
        "divider": ft.colors.GREY_200,
        "no_record": ft.colors.GREY_500,
    },
    "badges": {
        "vigente_bg": ft.colors.GREEN_100,
        "vigente_text": ft.colors.GREEN_800,
        "a_vencer_bg": ft.colors.YELLOW_100,
        "a_vencer_text": ft.colors.YELLOW_800,
        "vencida_bg": ft.colors.RED_100,
        "vencida_text": ft.colors.RED_800,
    },
    "actions": {
        "view": ft.colors.INDIGO_600,
        "view_hover": ft.colors.INDIGO_900,
        "edit": ft.colors.GREY_600,
        "edit_hover": ft.colors.GREY_900,
        "delete": ft.colors.RED_600,
        "delete_hover": ft.colors.RED_900,
    },
}

DARK = {
    "app_bg": ft.colors.GREY_900,
    "text": ft.colors.WHITE,
    "sidebar": {
        "bg": ft.colors.GREY_800,
        "title": ft.colors.INDIGO_500,
        "link": ft.colors.GREY_300,
        "link_hover_bg": ft.colors.INDIGO_900,
        "link_hover_text": ft.colors.INDIGO_300,
        "link_active_bg": ft.colors.INDIGO_900,
        "link_active_text": ft.colors.INDIGO_300,
        "toggle_bg": ft.colors.GREY_700,
        "icon_sun": ft.colors.AMBER_400,
        "icon_moon": ft.colors.GREY_500,
    },
    "header": {
        "bg": ft.colors.GREY_800,
        "title": ft.colors.WHITE,
        "search_bg": ft.colors.GREY_700,
        "search_text": ft.colors.WHITE,
        "search_placeholder": ft.colors.WHITE,
        "search_icon": ft.colors.GREY_400,
        "search_focus": ft.colors.INDIGO_500,
        "button_bg": ft.colors.INDIGO_600,
        "button_text": ft.colors.WHITE,
        "button_hover_bg": ft.colors.INDIGO_700,
    },
    "tabs": {
        "border": ft.colors.GREY_700,
        "text": ft.colors.GREY_400,
        "hover": ft.colors.GREY_200,
        "active_border": ft.colors.INDIGO_500,
        "active_text": ft.colors.INDIGO_400,
    },
    "table": {
        "card_bg": ft.colors.GREY_800,
        "title_text": ft.colors.WHITE,
        "header_border": ft.colors.GREY_700,
        "header_bg": ft.colors.GREY_700,
        "header_text": ft.colors.GREY_300,
        "number_text": ft.colors.WHITE,
        "other_text": ft.colors.GREY_400,
        "divider": ft.colors.GREY_700,
        "no_record": ft.colors.GREY_400,
    },
    "badges": {
        "vigente_bg": ft.colors.GREEN_900,
        "vigente_text": ft.colors.GREEN_300,
        "a_vencer_bg": ft.colors.YELLOW_900,
        "a_vencer_text": ft.colors.YELLOW_300,
        "vencida_bg": ft.colors.RED_900,
        "vencida_text": ft.colors.RED_300,
    },
    "actions": {
        "view": ft.colors.INDIGO_400,
        "view_hover": ft.colors.INDIGO_300,
        "edit": ft.colors.GREY_400,
        "edit_hover": ft.colors.GREY_300,
        "delete": ft.colors.RED_400,
        "delete_hover": ft.colors.RED_300,
    },
}


COLORS = {
    "light": LIGHT,
    "dark": DARK,
}

def get_theme(mode: ft.ThemeMode | str):
    if isinstance(mode, ft.ThemeMode):
        mode = "dark" if mode == ft.ThemeMode.DARK else "light"
    return COLORS.get(str(mode).lower(), LIGHT)

__all__ = ["LIGHT", "DARK", "COLORS", "get_theme"]
