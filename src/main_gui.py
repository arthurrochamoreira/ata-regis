import flet as ft
from components.sidebar import create_sidebar
from components.appbar import create_appbar
from views.dashboard import create_dashboard
from views.atas_view import create_atas_view
from views.vencimentos_view import create_vencimentos_view
from widgets.ata_form import create_ata_form
from widgets.details_card import create_details_card


class AtaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = "dashboard"
        self.is_sidebar_open = True
        self.filtro = "Todas"
        self.page.title = "Atas de Registro de Preços"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.on_resize = self.on_resize
        self.page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)
        self.build_layout()

    # Theme -------------------------------------------------
    def toggle_theme(self, e=None):
        self.page.theme_mode = (
            ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        self.page.update()

    def change_primary_color(self, color_name: str):
        color = getattr(ft.colors, color_name)
        self.page.theme = ft.Theme(color_scheme_seed=color)
        self.page.update()

    # Layout ------------------------------------------------
    def build_layout(self):
        self.sidebar = create_sidebar(self)
        self.view_container = ft.Container(expand=True)
        self.page.appbar = create_appbar(self)
        self.root = ft.Row([self.sidebar, self.view_container], expand=True)
        self.page.add(self.root)
        self.render_view()

    def render_view(self):
        if self.current_view == "dashboard":
            content = create_dashboard(self)
        elif self.current_view == "atas":
            content = create_atas_view(self)
        elif self.current_view == "vencimentos":
            content = create_vencimentos_view(self)
        elif self.current_view == "detalhes":
            content = create_details_card(self.selected_ata, self.back_to_list, self.edit_ata)
        else:
            content = ft.Text("View not found")
        self.view_container.content = content
        self.page.update()

    # Navigation --------------------------------------------
    def back_to_list(self, e=None):
        self.current_view = "atas"
        self.render_view()

    def show_details(self, ata):
        self.selected_ata = ata
        self.current_view = "detalhes"
        self.render_view()

    def edit_ata(self, e=None):
        self.open_new_ata_form()

    def open_new_ata_form(self):
        def close_dialog(e=None):
            self.page.dialog.open = False
            self.page.update()

        def save(data):
            close_dialog()

        dialog = create_ata_form(lambda e: close_dialog(), save)
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    # Tools placeholders ------------------------------------
    def check_alerts(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Verificando alertas..."))
        self.page.snack_bar.open = True
        self.page.update()

    def generate_report(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Gerando relatório..."))
        self.page.snack_bar.open = True
        self.page.update()

    def test_email(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Testando e-mail..."))
        self.page.snack_bar.open = True
        self.page.update()

    def check_system_status(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Status do sistema OK"))
        self.page.snack_bar.open = True
        self.page.update()

    # Responsive -------------------------------------------
    def on_resize(self, e):
        width = self.page.window_width
        if width < 600:
            self.is_sidebar_open = False
            self.sidebar.visible = False
            self.page.text_scale = 0.9
        else:
            self.sidebar.visible = True
            self.page.text_scale = 1
            if width > 1200:
                self.is_sidebar_open = True
            else:
                self.is_sidebar_open = False
        self.update_sidebar()
        self.page.update()

    def update_sidebar(self):
        self.root.controls[0] = create_sidebar(self)
        self.sidebar = self.root.controls[0]


def main(page: ft.Page):
    AtaApp(page)


if __name__ == "__main__":
    ft.app(target=main)
