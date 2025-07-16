import flet as ft
import database
import datetime
import re
from typing import List, Dict, Any

# ---------------------------------------------------------------
# Helpers de máscara viva que preservam o modelo de exemplo
# ---------------------------------------------------------------
def _aplicar_mascara(texto_digitado: str, mascara: str) -> str:
    """
    Recebe a string atual (com dígitos e a máscara) e devolve
    a máscara com os próximos dígitos substituindo caracteres
    alfanuméricos (0-9 ou letras) da esquerda para a direita.
    """
    digitos = re.sub(r'\D', '', texto_digitado)  # apenas números
    saida, i = [], 0
    for ch in mascara:
        if ch.isdigit() or ch.isalpha():  # é placeholder
            if i < len(digitos):
                saida.append(digitos[i])
                i += 1
            else:
                saida.append(ch)
        else:  # separador (/ - . etc.)
            saida.append(ch)
    return ''.join(saida)

def _handler_mascara(app: "AtaApp", mascara: str):
    """
    Fabrica o callback on_change que:
    1) aplica a máscara viva
    2) posiciona o cursor no próximo placeholder (0, D, M, A)
    """
    placeholders = {c for c in mascara if c.isdigit() or c.isalpha()}

    def _on_change(e):
        novo_valor = _aplicar_mascara(e.control.value, mascara)
        e.control.value = novo_valor

        # cursor → primeiro placeholder ainda não preenchido
        prox = next(
            (idx for idx, ch in enumerate(novo_valor) if ch in placeholders),
            len(novo_valor)
        )
        e.control.selection_start = e.control.selection_end = prox
        app.page.update()

    return _on_change

class AtaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Gerenciador de Atas de Registro de Preços"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600

        self.colors = {
            'primary_blue': '#0078d4', 'secondary_blue': '#deecf9',
            'status_active': '#107c10', 'status_warning': '#ff8c00',
            'status_expired': '#d13438', 'gray_50': '#faf9f8',
            'gray_100': '#f3f2f1', 'gray_200': '#edebe9',
            'gray_700': '#605e5c', 'gray_800': '#323130', 'white': '#ffffff'
        }
        
        self.atas = []
        self.current_edit_ata = None
        
        self.vigentes_column = None
        self.proximas_column = None
        self.vencidas_column = None
        self.modal = None
        
        self.setup_ui()
        # self.load_atas() # Carregamento de dados será chamado no final de setup_ui

    def setup_ui(self):
        """Configura a interface do usuário."""
        header = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ASSIGNMENT, color=self.colors['white'], size=24),
                        bgcolor=self.colors['primary_blue'], border_radius=8, padding=12, width=48, height=48
                    ),
                    ft.Column([
                        ft.Text("Atas de Registro de Preços", size=24, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.Text("Gerencie as atas em um painel centralizado", size=14, color=self.colors['gray_700'])
                    ], spacing=2)
                ], spacing=16),
                ft.ElevatedButton(
                    "Nova Ata", icon=ft.Icons.ADD, on_click=self.open_modal,
                    bgcolor=self.colors['primary_blue'], color=self.colors['white']
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=self.colors['white'], padding=ft.padding.symmetric(horizontal=32, vertical=16),
            border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
        )

        board_header = ft.Container(
            content=ft.Row([
                ft.Text("Painel de Controle", size=28, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                ft.Row([
                    ft.OutlinedButton("Filtrar", icon=ft.Icons.FILTER_LIST),
                    ft.OutlinedButton("Ordenar", icon=ft.Icons.SORT)
                ], spacing=8)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=32, vertical=24)
        )

        self.vigentes_column = self.create_column("Vigentes", self.colors['status_active'], 0)
        self.proximas_column = self.create_column("Próximas ao Vencimento", self.colors['status_warning'], 0)
        self.vencidas_column = self.create_column("Vencidas", self.colors['status_expired'], 0)

        columns_row = ft.Row([
            self.vigentes_column, self.proximas_column, self.vencidas_column
        ], spacing=24, expand=True, alignment=ft.MainAxisAlignment.START)

        main_content = ft.Container(
            content=ft.Column([
                board_header,
                ft.Container(content=columns_row, padding=ft.padding.symmetric(horizontal=32), expand=True)
            ], expand=True),
            bgcolor=self.colors['gray_50'], expand=True
        )

        self.modal = self.create_modal()
        self.page.add(
            ft.Column([header, main_content], expand=True, spacing=0)
        )
        # Dialogs devem ser atribuídos à propriedade ``page.dialog`` para serem exibidos corretamente
        self.page.dialog = self.modal
        self.load_atas()


    def create_column(self, title: str, color: str, count: int):
        """Cria uma coluna do Kanban."""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Container(width=12, height=12, bgcolor=color, border_radius=6),
                            ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                            ft.Container(
                                content=ft.Text(str(count), size=12, weight=ft.FontWeight.W_600, color=self.colors['gray_700']),
                                bgcolor=self.colors['gray_200'], padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=12
                            )
                        ], spacing=8),
                        ft.IconButton(ft.Icons.MORE_HORIZ, icon_color=self.colors['gray_700'])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.all(16), border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
                ),
                ft.Container(
                    content=ft.Column([], spacing=12, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.all(16), expand=True
                )
            ], spacing=0),
            bgcolor=self.colors['white'], border_radius=12,
            border=ft.border.all(1, self.colors['gray_200']), width=320, height=600
        )

    def create_modal(self):
        """Cria o modal para adicionar/editar atas."""
        # Número da Ata – usa a dica existente como máscara
        self.numero_ata_field = ft.TextField(
            label="Número da Ata",
            value="NNNN/NNNN",  # << ALTERAÇÃO AQUI
            on_change=_handler_mascara(self, "NNNN/NNNN") # << ALTERAÇÃO AQUI
        )
        self.documento_sei_field = ft.TextField(label="Documento SEI", hint_text="Ex: 12345.67890/2024-11")
        self.objeto_field = ft.TextField(label="Objeto", hint_text="Descrição do objeto da ata")
        # Datas – máscara com letras D/M/A
        self.data_assinatura_field = ft.TextField(label="Data de Assinatura", value="DD/MM/AAAA", on_change=_handler_mascara(self, "DD/MM/AAAA"))
        self.data_vigencia_field = ft.TextField(label="Data de Vigência", value="DD/MM/AAAA", on_change=_handler_mascara(self, "DD/MM/AAAA"))
        self.fornecedor_field = ft.TextField(label="Nome do Fornecedor", hint_text="Nome da empresa fornecedora")
        
        self.telefones_list = ft.Column([], spacing=8)
        self.emails_list = ft.Column([], spacing=8)
        self.items_list = ft.Column([], spacing=12)

        modal_content = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("Nova Ata", size=24, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.IconButton(ft.Icons.CLOSE, on_click=self.close_modal, icon_color=self.colors['gray_700'])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.all(24), border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Informações Básicas", size=18, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.Row([self.numero_ata_field, self.documento_sei_field], spacing=16),
                        self.objeto_field,
                        ft.Row([self.data_assinatura_field, self.data_vigencia_field], spacing=16),
                        ft.Divider(height=32),
                        ft.Text("Dados do Fornecedor", size=18, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        self.fornecedor_field,
                        ft.Row([
                            ft.Column([
                                ft.Text("Telefones", size=14, weight=ft.FontWeight.W_500), self.telefones_list,
                                ft.OutlinedButton("Adicionar Telefone", icon=ft.Icons.ADD, on_click=self.add_telefone_field)
                            ], expand=True),
                            ft.Column([
                                ft.Text("E-mails", size=14, weight=ft.FontWeight.W_500), self.emails_list,
                                ft.OutlinedButton("Adicionar E-mail", icon=ft.Icons.ADD, on_click=self.add_email_field)
                            ], expand=True)
                        ], spacing=24),
                        ft.Divider(height=32),
                        ft.Row([
                            ft.Text("Itens da Ata", size=18, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                            ft.OutlinedButton("Adicionar Item", icon=ft.Icons.ADD, on_click=self.add_item_field)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.items_list
                    ], spacing=16, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.all(24), expand=True
                ),
                ft.Container(
                    content=ft.Row([
                        ft.OutlinedButton("Cancelar", on_click=self.close_modal),
                        ft.ElevatedButton("Salvar", icon=ft.Icons.SAVE, on_click=self.save_ata,
                                         bgcolor=self.colors['primary_blue'], color=self.colors['white'])
                    ], alignment=ft.MainAxisAlignment.END, spacing=12),
                    padding=ft.padding.all(24), border=ft.border.only(top=ft.BorderSide(1, self.colors['gray_200']))
                )
            ], spacing=0),
            bgcolor=self.colors['white'], border_radius=12, width=800, height=700
        )
        return ft.AlertDialog(modal=True, content=modal_content, content_padding=0)

    def create_card(self, ata: Dict[str, Any]) -> ft.Container:
        """Cria um card para uma ata."""
        today = datetime.date.today()
        vigencia_date = datetime.datetime.strptime(ata['dataVigencia'], "%Y-%m-%d").date()
        assinatura_date = datetime.datetime.strptime(ata['dataAssinatura'], "%Y-%m-%d").date()
        is_expired = vigencia_date < today
        total_duration = max(1, (vigencia_date - assinatura_date).days)
        elapsed_duration = max(0, (today - assinatura_date).days)
        progress = min(100, (elapsed_duration / total_duration) * 100) if not is_expired else 100
        
        if vigencia_date < today:
            status_text, status_color = "Vencida", self.colors['status_expired']
        elif vigencia_date <= today + datetime.timedelta(days=90):
            status_text, status_color = "Vence em breve", self.colors['status_warning']
        else:
            status_text, status_color = "Vigente", self.colors['status_active']

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(ata['objeto'], size=16, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.Text(f"Ata: {ata['numeroAta']} | SEI: {ata['documentoSei']}", size=12, color=self.colors['gray_700'])
                    ], expand=True),
                    ft.Container(
                        content=ft.Text(status_text, size=10, weight=ft.FontWeight.W_600, color=self.colors['white']),
                        bgcolor=status_color, padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=12
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Column([
                    ft.Row([
                        ft.Text("Progresso", size=12, color=self.colors['gray_700']),
                        ft.Text(f"Venc.: {vigencia_date.strftime('%d/%m/%Y')}", size=12, color=self.colors['gray_700'])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.ProgressBar(value=progress/100, bgcolor=self.colors['gray_200'], color=self.colors['primary_blue'])
                ], spacing=4),
                ft.Text(f"Fornecedor: {ata['fornecedor']}", size=14, color=self.colors['gray_700']),
                ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=self.colors['primary_blue'], on_click=lambda e, ata_id=ata['id']: self.edit_ata(ata_id), tooltip="Editar"),
                    ft.IconButton(ft.Icons.DELETE, icon_color=self.colors['status_expired'], on_click=lambda e, ata_id=ata['id']: self.delete_ata(ata_id), tooltip="Excluir")
                ], alignment=ft.MainAxisAlignment.END)
            ], spacing=12),
            bgcolor=self.colors['white'], border=ft.border.all(1, self.colors['gray_200']), border_radius=8, padding=ft.padding.all(16)
        )

    def load_atas(self):
        # Garante que o banco de dados e a tabela existam
        database.init_db()
        self.atas = database.get_all_atas()
        if self.page.controls: # Garante que a UI esteja pronta
            self.update_columns()

    def update_columns(self):
        today = datetime.date.today()
        ninety_days_from_now = today + datetime.timedelta(days=90)
        vigentes, proximas, vencidas = [], [], []
        for ata in self.atas:
            try:
                vigencia_date = datetime.datetime.strptime(ata['dataVigencia'], "%Y-%m-%d").date()
                if vigencia_date < today: vencidas.append(ata)
                elif vigencia_date <= ninety_days_from_now: proximas.append(ata)
                else: vigentes.append(ata)
            except (ValueError, KeyError): continue
        self.update_column_count(self.vigentes_column, len(vigentes))
        self.update_column_count(self.proximas_column, len(proximas))
        self.update_column_count(self.vencidas_column, len(vencidas))
        self.update_column_cards(self.vigentes_column, vigentes)
        self.update_column_cards(self.proximas_column, proximas)
        self.update_column_cards(self.vencidas_column, vencidas)
        if self.page.controls: self.page.update()

    def update_column_count(self, column: ft.Container, count: int):
        if column:
            header_row = column.content.controls[0].content
            count_container = header_row.controls[0].controls[2]
            count_container.content.value = str(count)

    def update_column_cards(self, column: ft.Container, atas: List[Dict[str, Any]]):
        if column:
            cards_column = column.content.controls[1].content
            cards_column.controls.clear()
            for ata in atas:
                cards_column.controls.append(self.create_card(ata))

    def open_modal(self, e=None):
        self.current_edit_ata = None
        self.clear_modal_fields()
        self.modal.content.content.controls[0].content.controls[0].value = "Nova Ata"
        # Garantir que o diálogo esteja atribuído corretamente à página
        self.page.dialog = self.modal
        self.modal.open = True
        self.page.update()

    def close_modal(self, e=None):
        self.modal.open = False
        # Remove a referência do diálogo para evitar conflitos com outros diálogos
        self.page.dialog = None
        self.page.update()

    def clear_modal_fields(self):
        """Limpa os campos do modal e remove mensagens de erro."""
        fields_with_mask = [self.numero_ata_field, self.data_assinatura_field, self.data_vigencia_field]
        simple_fields = [self.documento_sei_field, self.objeto_field, self.fornecedor_field]
        
        for field in fields_with_mask:
            field.value = ""
            field.error_text = None
            # Dispara o on_change para restaurar a máscara
            field.on_change(ft.ControlEvent(target=field.uid, name="change", data="", control=field, page=self.page))
            
        for field in simple_fields:
            field.value = ""
            field.error_text = None
        
        self.telefones_list.controls.clear()
        self.emails_list.controls.clear()
        self.items_list.controls.clear()
        self.page.update()

    def add_telefone_field(self, e=None):
        telefone_field = ft.Row([
            ft.TextField(hint_text="Telefone", expand=True),
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e: self.remove_field(self.telefones_list, e.control.data))
        ])
        telefone_field.controls[1].data = telefone_field
        self.telefones_list.controls.append(telefone_field)
        self.page.update()

    def add_email_field(self, e=None):
        email_field = ft.Row([
            ft.TextField(hint_text="E-mail", expand=True),
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e: self.remove_field(self.emails_list, e.control.data))
        ])
        email_field.controls[1].data = email_field
        self.emails_list.controls.append(email_field)
        self.page.update()

    def add_item_field(self, e=None):
        item_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"Item {len(self.items_list.controls) + 1}", size=16, weight=ft.FontWeight.W_500),
                    ft.IconButton(ft.Icons.DELETE, icon_color=self.colors['status_expired'], on_click=lambda e: self.remove_field(self.items_list, e.control.data))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.TextField(label="Descrição", hint_text="Descrição do item"),
                ft.Row([
                    ft.TextField(label="Quantidade", hint_text="0", expand=True, keyboard_type=ft.KeyboardType.NUMBER),
                    ft.TextField(label="Valor Unitário (R$)", hint_text="0.00", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
                ], spacing=16)
            ], spacing=8),
            bgcolor=self.colors['gray_50'], border=ft.border.all(1, self.colors['gray_200']),
            border_radius=8, padding=ft.padding.all(16)
        )
        item_container.content.controls[0].controls[1].data = item_container
        self.items_list.controls.append(item_container)
        self.page.update()

    def remove_field(self, parent_list: ft.Column, field_to_remove):
        if field_to_remove in parent_list.controls:
            parent_list.controls.remove(field_to_remove)
            if parent_list == self.items_list:
                for i, item_container in enumerate(parent_list.controls):
                    item_container.content.controls[0].controls[0].value = f"Item {i + 1}"
            self.page.update()

    def save_ata(self, e=None):
        """Salva uma ata após validar os campos."""
        is_valid = True
        for field in [self.numero_ata_field, self.documento_sei_field, self.objeto_field, self.data_assinatura_field, self.data_vigencia_field, self.fornecedor_field]:
            field.error_text = None

        if re.search(r'[N]', self.numero_ata_field.value): # << ALTERAÇÃO AQUI
            self.numero_ata_field.error_text = "Preencha todos os dígitos."
            is_valid = False
            
        for campo in (self.data_assinatura_field, self.data_vigencia_field):
            if re.search(r'[DMA]', campo.value):
                campo.error_text = "Data incompleta."
                is_valid = False

        data_assinatura_obj, data_vigencia_obj = None, None
        try: data_assinatura_obj = datetime.datetime.strptime(self.data_assinatura_field.value, "%d/%m/%Y")
        except ValueError:
            if not re.search(r'[DMA]', self.data_assinatura_field.value):
                self.data_assinatura_field.error_text = "Formato inválido."
                is_valid = False
        
        try: data_vigencia_obj = datetime.datetime.strptime(self.data_vigencia_field.value, "%d/%m/%Y")
        except ValueError:
            if not re.search(r'[DMA]', self.data_vigencia_field.value):
                self.data_vigencia_field.error_text = "Formato inválido."
                is_valid = False

        if data_assinatura_obj and data_vigencia_obj and data_vigencia_obj <= data_assinatura_obj:
            self.data_vigencia_field.error_text = "Vigência deve ser posterior à assinatura."
            is_valid = False

        self.page.update()
        if not is_valid:
            self.show_snackbar("Por favor, corrija os erros no formulário.", self.colors['status_expired'])
            return

        try:
            ata_data = {
                'numeroAta': self.numero_ata_field.value.strip(),
                'documentoSei': self.documento_sei_field.value.strip(),
                'objeto': self.objeto_field.value.strip(),
                'dataAssinatura': data_assinatura_obj.strftime("%Y-%m-%d"),
                'dataVigencia': data_vigencia_obj.strftime("%Y-%m-%d"),
                'fornecedor': self.fornecedor_field.value.strip(),
                'telefonesFornecedor': [row.controls[0].value.strip() for row in self.telefones_list.controls if row.controls[0].value.strip()],
                'emailsFornecedor': [row.controls[0].value.strip() for row in self.emails_list.controls if row.controls[0].value.strip()],
                'items': [],
                'updatedAt': datetime.datetime.now().isoformat()
            }
            
            # ... Lógica para coletar itens da ata ...

            if self.current_edit_ata:
                database.update_ata(self.current_edit_ata, ata_data)
            else:
                ata_data['createdAt'] = datetime.datetime.now().isoformat()
                database.insert_ata(ata_data)

            self.load_atas()
            self.close_modal()
            self.show_snackbar("Ata salva com sucesso!", self.colors['status_active'])
            
        except Exception as ex:
            self.show_snackbar(f"Erro inesperado ao salvar: {str(ex)}", self.colors['status_expired'])

    def edit_ata(self, ata_id: int):
        ata = next((a for a in self.atas if a['id'] == ata_id), None)
        if ata:
            self.current_edit_ata = ata_id
            self.clear_modal_fields()
            self.populate_modal_fields(ata)
            self.modal.content.content.controls[0].content.controls[0].value = f"Editar Ata {ata.get('numeroAta', '')}"
            self.modal.open = True
            self.page.update()

    def populate_modal_fields(self, ata: Dict[str, Any]):
        self.numero_ata_field.value = ata.get('numeroAta', '')
        self.documento_sei_field.value = ata.get('documentoSei', '')
        self.objeto_field.value = ata.get('objeto', '')
        self.fornecedor_field.value = ata.get('fornecedor', '')
        
        try: self.data_assinatura_field.value = datetime.datetime.strptime(ata['dataAssinatura'], '%Y-%m-%d').strftime('%d/%m/%Y')
        except (ValueError, KeyError): self.data_assinatura_field.value = ""
        try: self.data_vigencia_field.value = datetime.datetime.strptime(ata['dataVigencia'], '%Y-%m-%d').strftime('%d/%m/%Y')
        except (ValueError, KeyError): self.data_vigencia_field.value = ""

        # Dispara o on_change para formatar os campos com máscara
        for field in [self.numero_ata_field, self.data_assinatura_field, self.data_vigencia_field]:
             field.on_change(ft.ControlEvent(target=field.uid, name="change", data=field.value, control=field, page=self.page))

        # ... Lógica para popular telefones, emails e itens ...
        self.page.update()

    def delete_ata(self, ata_id: int):
        def confirm_delete(e):
            try:
                database.delete_ata(ata_id)
                self.load_atas()
                self.show_snackbar("Ata excluída com sucesso!", self.colors['status_active'])
            except Exception as ex:
                self.show_snackbar(f"Erro ao excluir ata: {str(ex)}", self.colors['status_expired'])
            finally:
                confirm_dialog.open = False
                self.page.update()
        def cancel_delete(e):
            confirm_dialog.open = False
            self.page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Tem certeza que deseja excluir esta ata? Esta ação não pode ser desfeita."),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete),
                ft.TextButton("Excluir", on_click=confirm_delete, style=ft.ButtonStyle(color=self.colors['status_expired']))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def show_snackbar(self, message: str, color: str):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=self.colors['white']),
            bgcolor=color, duration=4000
        )
        self.page.snack_bar.open = True
        self.page.update()

def main(page: ft.Page):
    app = AtaApp(page)

if __name__ == "__main__":
    # A linha "database.init_db()" foi removida daqui.
    ft.app(target=main)