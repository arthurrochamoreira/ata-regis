import flet as ft

# Color schemes for light and dark modes
LIGHT = {
    # Application
    "app_bg": ft.colors.GREY_100,
    "app_text": ft.colors.GREY_900,
    # Sidebar
    "sidebar_bg": ft.colors.WHITE,
    "sidebar_title": ft.colors.INDIGO_500,
    "nav_link": ft.colors.GREY_700,
    "nav_link_hover_bg": ft.colors.INDIGO_100,
    "nav_link_hover_text": ft.colors.INDIGO_600,
    "nav_link_active_bg": ft.colors.INDIGO_50,
    "nav_link_active_text": ft.colors.INDIGO_600,
    "toggle_bg": ft.colors.GREY_100,
    "toggle_sun": ft.colors.AMBER_400,
    "toggle_moon": ft.colors.GREY_500,
    # Header
    "header_bg": ft.colors.WHITE,
    "header_title": ft.colors.GREY_900,
    "search_bg": ft.colors.GREY_100,
    "search_icon": ft.colors.GREY_400,
    "search_focus_border": ft.colors.INDIGO_500,
    "new_button_bg": ft.colors.INDIGO_600,
    "new_button_text": ft.colors.WHITE,
    "new_button_hover": ft.colors.INDIGO_700,
    # Tabs
    "tabs_border": ft.colors.GREY_200,
    "tab_text": ft.colors.GREY_500,
    "tab_text_hover": ft.colors.GREY_700,
    "tab_active_border": ft.colors.INDIGO_500,
    "tab_active_text": ft.colors.INDIGO_600,
    # Tables
    "table_bg": ft.colors.WHITE,
    "table_title": ft.colors.GREY_900,
    "table_header_border": ft.colors.GREY_200,
    "table_header_bg": ft.colors.GREY_50,
    "table_header_text": ft.colors.GREY_500,
    "table_number": ft.colors.GREY_900,
    "table_text": ft.colors.GREY_500,
    "table_divider": ft.colors.GREY_200,
    "table_no_records": ft.colors.GREY_500,
    # Badges
    "badge_vigente_bg": ft.colors.GREEN_100,
    "badge_vigente_text": ft.colors.GREEN_800,
    "badge_avencer_bg": ft.colors.YELLOW_100,
    "badge_avencer_text": ft.colors.YELLOW_800,
    "badge_vencida_bg": ft.colors.RED_100,
    "badge_vencida_text": ft.colors.RED_800,
    # Action buttons
    "action_ver": ft.colors.INDIGO_600,
    "action_ver_hover": ft.colors.INDIGO_900,
    "action_editar": ft.colors.GREY_600,
    "action_editar_hover": ft.colors.GREY_900,
    "action_excluir": ft.colors.RED_600,
    "action_excluir_hover": ft.colors.RED_900,
}

DARK = {
    # Application
    "app_bg": ft.colors.GREY_900,
    "app_text": ft.colors.WHITE,
    # Sidebar
    "sidebar_bg": ft.colors.GREY_800,
    "sidebar_title": ft.colors.INDIGO_500,
    "nav_link": ft.colors.GREY_300,
    "nav_link_hover_bg": ft.colors.INDIGO_900,
    "nav_link_hover_text": ft.colors.INDIGO_300,
    "nav_link_active_bg": ft.colors.INDIGO_900,
    "nav_link_active_text": ft.colors.INDIGO_300,
    "toggle_bg": ft.colors.GREY_700,
    "toggle_sun": ft.colors.AMBER_400,
    "toggle_moon": ft.colors.GREY_500,
    # Header
    "header_bg": ft.colors.GREY_800,
    "header_title": ft.colors.WHITE,
    "search_bg": ft.colors.GREY_700,
    "search_icon": ft.colors.GREY_400,
    "search_focus_border": ft.colors.INDIGO_500,
    "new_button_bg": ft.colors.INDIGO_600,
    "new_button_text": ft.colors.WHITE,
    "new_button_hover": ft.colors.INDIGO_700,
    # Tabs
    "tabs_border": ft.colors.GREY_700,
    "tab_text": ft.colors.GREY_400,
    "tab_text_hover": ft.colors.GREY_200,
    "tab_active_border": ft.colors.INDIGO_500,
    "tab_active_text": ft.colors.INDIGO_400,
    # Tables
    "table_bg": ft.colors.GREY_800,
    "table_title": ft.colors.WHITE,
    "table_header_border": ft.colors.GREY_700,
    "table_header_bg": ft.colors.GREY_700,
    "table_header_text": ft.colors.GREY_300,
    "table_number": ft.colors.WHITE,
    "table_text": ft.colors.GREY_400,
    "table_divider": ft.colors.GREY_700,
    "table_no_records": ft.colors.GREY_400,
    # Badges
    "badge_vigente_bg": ft.colors.GREEN_900,
    "badge_vigente_text": ft.colors.GREEN_300,
    "badge_avencer_bg": ft.colors.YELLOW_900,
    "badge_avencer_text": ft.colors.YELLOW_300,
    "badge_vencida_bg": ft.colors.RED_900,
    "badge_vencida_text": ft.colors.RED_300,
    # Action buttons
    "action_ver": ft.colors.INDIGO_400,
    "action_ver_hover": ft.colors.INDIGO_300,
    "action_editar": ft.colors.GREY_400,
    "action_editar_hover": ft.colors.GREY_300,
    "action_excluir": ft.colors.RED_400,
    "action_excluir_hover": ft.colors.RED_300,
}


def scheme(page: ft.Page) -> dict:
    """Return color scheme based on current page theme mode."""
    return DARK if page.theme_mode == ft.ThemeMode.DARK else LIGHT
