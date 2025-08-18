import flet as ft
from theme import colors as C

STATUS_INFO = {
    "vigente": {
        "title": "Atas Vigentes",
        "filter": "Vigentes",
        "icon": ft.icons.CHECK_CIRCLE,
        "icon_color": C.SUCCESS_TEXT,
        "icon_bg": C.SUCCESS_BG,
        "button_color": C.SUCCESS_TEXT,
    },
    "a_vencer": {
        "title": "Atas a Vencer",
        "filter": "A Vencer",
        "icon": ft.icons.WARNING_AMBER_ROUNDED,
        "icon_color": C.WARNING_TEXT,
        "icon_bg": C.WARNING_BG,
        "button_color": C.WARNING_TEXT,
    },
    "vencida": {
        "title": "Atas Vencidas",
        "filter": "Vencidas",
        "icon": ft.icons.CANCEL,
        "icon_color": C.ERROR_TEXT,
        "icon_bg": C.ERROR_BG,
        "button_color": C.ERROR_TEXT,
    },
}
