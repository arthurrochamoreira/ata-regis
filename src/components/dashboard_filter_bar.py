import flet as ft
from theme.tokens import TOKENS as T


def make_filter_bar(*, on_search, on_clear, on_sort_change, initial_query: str = "", initial_sort: str = "recentes"):
    search_field = ft.TextField(value=initial_query, on_change=on_search, expand=True)
    clear_button = ft.IconButton(ft.icons.CLEAR, on_click=on_clear)
    sort_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("recentes"), ft.dropdown.Option("antigos")],
        value=initial_sort,
        on_change=on_sort_change,
    )
    return ft.Row(
        [search_field, clear_button, sort_dropdown],
        spacing=T.spacing.SPACE_4,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
