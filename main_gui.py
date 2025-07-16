import flet as ft
import database
import datetime
from typing import List, Dict, Any

class AtaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Gerenciador de Atas de Registro de Preços"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        
        # Cores do Microsoft Planner
        self.colors = {
            'primary_blue': '#0078d4',
            'secondary_blue': '#deecf9',
            'status_active': '#107c10',
            'status_warning': '#ff8c00',
            'status_expired': '#d13438',
            'gray_50': '#faf9f8',
            'gray_100': '#f3f2f1',
            'gray_200': '#edebe9',
            'gray_700': '#605e5c',
            'gray_800': '#323130',
            'white': '#ffffff'
        }
        
        # Estado da aplicação
        self.atas = []
        self.current_edit_ata = None
        
        # Componentes da UI
        self.vigentes_column = None
        self.proximas_column = None
        self.vencidas_column = None
        self.modal = None
        
        self.setup_ui()
        self.load_atas()

    def setup_ui(self):
        """Configura a interface do usuário."""
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ASSIGNMENT, color=self.colors['white'], size=24),
                        bgcolor=self.colors['primary_blue'],
                        border_radius=8,
                        padding=12,
                        width=48,
                        height=48
                    ),
                    ft.Column([
                        ft.Text("Atas de Registro de Preços", size=24, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.Text("Gerencie as atas em um painel centralizado", size=14, color=self.colors['gray_700'])
                    ], spacing=2)
                ], spacing=16),
                ft.ElevatedButton(
                    "Nova Ata",
                    icon=ft.Icons.ADD,
                    on_click=self.open_modal,
                    bgcolor=self.colors['primary_blue'],
                    color=self.colors['white']
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=self.colors['white'],
            padding=ft.padding.symmetric(horizontal=32, vertical=16),
            border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
        )

        # Board Header
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

        # Kanban Columns
        self.vigentes_column = self.create_column("Vigentes", self.colors['status_active'], 0)
        self.proximas_column = self.create_column("Próximas ao Vencimento", self.colors['status_warning'], 0)
        self.vencidas_column = self.create_column("Vencidas", self.colors['status_expired'], 0)

        columns_row = ft.Row([
            self.vigentes_column,
            self.proximas_column,
            self.vencidas_column
        ], spacing=24, expand=True, alignment=ft.MainAxisAlignment.START)

        # Main Content
        main_content = ft.Container(
            content=ft.Column([
                board_header,
                ft.Container(
                    content=columns_row,
                    padding=ft.padding.symmetric(horizontal=32),
                    expand=True
                )
            ], expand=True),
            bgcolor=self.colors['gray_50'],
            expand=True
        )

        # Modal
        self.modal = self.create_modal()

        # Page Layout
        self.page.add(
            ft.Column([
                header,
                main_content
            ], expand=True, spacing=0),
            self.modal
        )

    def create_column(self, title: str, color: str, count: int):
        """Cria uma coluna do Kanban."""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Container(
                                width=12,
                                height=12,
                                bgcolor=color,
                                border_radius=6
                            ),
                            ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                            ft.Container(
                                content=ft.Text(str(count), size=12, weight=ft.FontWeight.W_600, color=self.colors['gray_700']),
                                bgcolor=self.colors['gray_200'],
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=12
                            )
                        ], spacing=8),
                        ft.IconButton(ft.Icons.MORE_HORIZ, icon_color=self.colors['gray_700'])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.all(16),
                    border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
                ),
                ft.Container(
                    content=ft.Column([], spacing=12, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.all(16),
                    expand=True
                )
            ], spacing=0),
            bgcolor=self.colors['white'],
            border_radius=12,
            border=ft.border.all(1, self.colors['gray_200']),
            width=320,
            height=600
        )

    def create_modal(self):
        """Cria o modal para adicionar/editar atas."""
        # Campos do formulário
        self.numero_ata_field = ft.TextField(label="Número da Ata", hint_text="Ex: 0016/2024")
        self.documento_sei_field = ft.TextField(label="Documento SEI", hint_text="Ex: 12345.67890/2024-11")
        self.objeto_field = ft.TextField(label="Objeto", hint_text="Descrição do objeto da ata")
        self.data_assinatura_field = ft.TextField(label="Data de Assinatura", hint_text="AAAA-MM-DD")
        self.data_vigencia_field = ft.TextField(label="Data de Vigência", hint_text="AAAA-MM-DD")
        self.fornecedor_field = ft.TextField(label="Nome do Fornecedor", hint_text="Nome da empresa fornecedora")
        
        # Listas dinâmicas
        self.telefones_list = ft.Column([], spacing=8)
        self.emails_list = ft.Column([], spacing=8)
        self.items_list = ft.Column([], spacing=12)

        modal_content = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text("Nova Ata", size=24, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.IconButton(ft.Icons.CLOSE, on_click=self.close_modal, icon_color=self.colors['gray_700'])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.all(24),
                    border=ft.border.only(bottom=ft.BorderSide(1, self.colors['gray_200']))
                ),
                
                # Content
                ft.Container(
                    content=ft.Column([
                        # Informações Básicas
                        ft.Text("Informações Básicas", size=18, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.Row([self.numero_ata_field, self.documento_sei_field], spacing=16),
                        self.objeto_field,
                        ft.Row([self.data_assinatura_field, self.data_vigencia_field], spacing=16),
                        
                        ft.Divider(height=32),
                        
                        # Dados do Fornecedor
                        ft.Text("Dados do Fornecedor", size=18, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        self.fornecedor_field,
                        
                        ft.Row([
                            ft.Column([
                                ft.Text("Telefones", size=14, weight=ft.FontWeight.W_500),
                                self.telefones_list,
                                ft.OutlinedButton("Adicionar Telefone", icon=ft.Icons.ADD, on_click=self.add_telefone_field)
                            ], expand=True),
                            ft.Column([
                                ft.Text("E-mails", size=14, weight=ft.FontWeight.W_500),
                                self.emails_list,
                                ft.OutlinedButton("Adicionar E-mail", icon=ft.Icons.ADD, on_click=self.add_email_field)
                            ], expand=True)
                        ], spacing=24),
                        
                        ft.Divider(height=32),
                        
                        # Itens da Ata
                        ft.Row([
                            ft.Text("Itens da Ata", size=18, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                            ft.OutlinedButton("Adicionar Item", icon=ft.Icons.ADD, on_click=self.add_item_field)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.items_list
                    ], spacing=16, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.all(24),
                    expand=True
                ),
                
                # Footer
                ft.Container(
                    content=ft.Row([
                        ft.OutlinedButton("Cancelar", on_click=self.close_modal),
                        ft.ElevatedButton(
                            "Salvar",
                            icon=ft.Icons.SAVE,
                            on_click=self.save_ata,
                            bgcolor=self.colors['primary_blue'],
                            color=self.colors['white']
                        )
                    ], alignment=ft.MainAxisAlignment.END, spacing=12),
                    padding=ft.padding.all(24),
                    border=ft.border.only(top=ft.BorderSide(1, self.colors['gray_200']))
                )
            ], spacing=0),
            bgcolor=self.colors['white'],
            border_radius=12,
            width=800,
            height=600
        )

        return ft.AlertDialog(
            modal=True,
            content=modal_content,
            content_padding=0
        )

    def create_card(self, ata: Dict[str, Any]) -> ft.Container:
        """Cria um card para uma ata."""
        # Calcular status e progresso
        today = datetime.date.today()
        vigencia_date = datetime.datetime.strptime(ata['dataVigencia'], "%Y-%m-%d").date()
        assinatura_date = datetime.datetime.strptime(ata['dataAssinatura'], "%Y-%m-%d").date()
        
        is_expired = vigencia_date < today
        total_duration = max(1, (vigencia_date - assinatura_date).days)
        elapsed_duration = max(0, (today - assinatura_date).days)
        progress = min(100, (elapsed_duration / total_duration) * 100) if not is_expired else 100
        
        # Status
        if vigencia_date < today:
            status_text = "Vencida"
            status_color = self.colors['status_expired']
        elif vigencia_date <= today + datetime.timedelta(days=90):
            status_text = "Vence em breve"
            status_color = self.colors['status_warning']
        else:
            status_text = "Vigente"
            status_color = self.colors['status_active']

        return ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Column([
                        ft.Text(ata['objeto'], size=16, weight=ft.FontWeight.W_600, color=self.colors['gray_800']),
                        ft.Text(f"Ata: {ata['numeroAta']} | SEI: {ata['documentoSei']}", size=12, color=self.colors['gray_700'])
                    ], expand=True),
                    ft.Container(
                        content=ft.Text(status_text, size=10, weight=ft.FontWeight.W_600, color=self.colors['white']),
                        bgcolor=status_color,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=12
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                # Progress
                ft.Column([
                    ft.Row([
                        ft.Text("Progresso", size=12, color=self.colors['gray_700']),
                        ft.Text(f"Venc.: {vigencia_date.strftime('%d/%m/%Y')}", size=12, color=self.colors['gray_700'])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.ProgressBar(value=progress/100, bgcolor=self.colors['gray_200'], color=self.colors['primary_blue'])
                ], spacing=4),
                
                # Fornecedor
                ft.Text(f"Fornecedor: {ata['fornecedor']}", size=14, color=self.colors['gray_700']),
                
                # Actions
                ft.Row([
                    ft.IconButton(
                        ft.Icons.EDIT,
                        icon_color=self.colors['primary_blue'],
                        on_click=lambda e, ata_id=ata['id']: self.edit_ata(ata_id),
                        tooltip="Editar"
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        icon_color=self.colors['status_expired'],
                        on_click=lambda e, ata_id=ata['id']: self.delete_ata(ata_id),
                        tooltip="Excluir"
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ], spacing=12),
            bgcolor=self.colors['white'],
            border=ft.border.all(1, self.colors['gray_200']),
            border_radius=8,
            padding=ft.padding.all(16)
        )

    def load_atas(self):
        """Carrega as atas do banco de dados."""
        self.atas = database.get_all_atas()
        self.update_columns()

    def update_columns(self):
        """Atualiza as colunas do Kanban com as atas."""
        today = datetime.date.today()
        ninety_days_from_now = today + datetime.timedelta(days=90)
        
        vigentes = []
        proximas = []
        vencidas = []
        
        for ata in self.atas:
            try:
                vigencia_date = datetime.datetime.strptime(
                    ata['dataVigencia'], "%Y-%m-%d"
                ).date()
            except ValueError:
                # Skip invalid dates to avoid breaking UI
                continue

            if vigencia_date < today:
                vencidas.append(ata)
            elif vigencia_date <= ninety_days_from_now:
                proximas.append(ata)
            else:
                vigentes.append(ata)
        
        # Atualizar contadores nos headers
        self.update_column_count(self.vigentes_column, len(vigentes))
        self.update_column_count(self.proximas_column, len(proximas))
        self.update_column_count(self.vencidas_column, len(vencidas))
        
        # Atualizar cards nas colunas
        self.update_column_cards(self.vigentes_column, vigentes)
        self.update_column_cards(self.proximas_column, proximas)
        self.update_column_cards(self.vencidas_column, vencidas)
        
        self.page.update()

    def update_column_count(self, column: ft.Container, count: int):
        """Atualiza o contador de uma coluna."""
        header_row = column.content.controls[0].content
        count_container = header_row.controls[0].controls[2]
        count_container.content.value = str(count)

    def update_column_cards(self, column: ft.Container, atas: List[Dict[str, Any]]):
        """Atualiza os cards de uma coluna."""
        content_container = column.content.controls[1]
        cards_column = content_container.content
        cards_column.controls.clear()
        
        for ata in atas:
            cards_column.controls.append(self.create_card(ata))

    def open_modal(self, e=None):
        """Abre o modal para adicionar uma nova ata."""
        self.current_edit_ata = None
        self.clear_modal_fields()
        self.modal.open = True
        self.page.update()

    def close_modal(self, e=None):
        """Fecha o modal."""
        self.modal.open = False
        self.page.update()

    def clear_modal_fields(self):
        """Limpa os campos do modal."""
        self.numero_ata_field.value = ""
        self.documento_sei_field.value = ""
        self.objeto_field.value = ""
        self.data_assinatura_field.value = ""
        self.data_vigencia_field.value = ""
        self.fornecedor_field.value = ""
        
        self.telefones_list.controls.clear()
        self.emails_list.controls.clear()
        self.items_list.controls.clear()

    def add_telefone_field(self, e=None):
        """Adiciona um campo de telefone."""
        telefone_field = ft.Row([
            ft.TextField(hint_text="Telefone", expand=True),
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e, row=None: self.remove_field(self.telefones_list, row))
        ])
        telefone_field.controls[1].data = telefone_field
        self.telefones_list.controls.append(telefone_field)
        self.page.update()

    def add_email_field(self, e=None):
        """Adiciona um campo de e-mail."""
        email_field = ft.Row([
            ft.TextField(hint_text="E-mail", expand=True),
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e, row=None: self.remove_field(self.emails_list, row))
        ])
        email_field.controls[1].data = email_field
        self.emails_list.controls.append(email_field)
        self.page.update()

    def add_item_field(self, e=None):
        """Adiciona um campo de item."""
        item_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"Item {len(self.items_list.controls) + 1}", size=16, weight=ft.FontWeight.W_500),
                    ft.IconButton(ft.Icons.DELETE, icon_color=self.colors['status_expired'], 
                                on_click=lambda e, container=None: self.remove_field(self.items_list, container))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.TextField(label="Descrição", hint_text="Descrição do item"),
                ft.Row([
                    ft.TextField(label="Quantidade", hint_text="0", expand=True),
                    ft.TextField(label="Valor Unitário (R$)", hint_text="0.00", expand=True)
                ], spacing=16)
            ], spacing=8),
            bgcolor=self.colors['gray_50'],
            border=ft.border.all(1, self.colors['gray_200']),
            border_radius=8,
            padding=ft.padding.all(16)
        )
        item_container.controls[0].controls[0].controls[1].data = item_container
        self.items_list.controls.append(item_container)
        self.page.update()

    def remove_field(self, parent_list: ft.Column, field_to_remove):
        """Remove um campo de uma lista."""
        if field_to_remove in parent_list.controls:
            parent_list.controls.remove(field_to_remove)
            self.page.update()

    def save_ata(self, e=None):
        """Salva uma ata."""
        try:
            # Coletar dados dos campos
            ata_data = {
                'numeroAta': self.numero_ata_field.value,
                'documentoSei': self.documento_sei_field.value,
                'objeto': self.objeto_field.value,
                'dataAssinatura': self.data_assinatura_field.value,
                'dataVigencia': self.data_vigencia_field.value,
                'fornecedor': self.fornecedor_field.value,
                'telefonesFornecedor': [row.controls[0].value for row in self.telefones_list.controls if row.controls[0].value],
                'emailsFornecedor': [row.controls[0].value for row in self.emails_list.controls if row.controls[0].value],
                'items': [],
                'createdAt': datetime.datetime.now().isoformat(),
                'updatedAt': datetime.datetime.now().isoformat()
            }

            # Validate date fields
            try:
                datetime.datetime.strptime(ata_data['dataAssinatura'], "%Y-%m-%d")
                datetime.datetime.strptime(ata_data['dataVigencia'], "%Y-%m-%d")
            except ValueError:
                self.show_snackbar(
                    "Datas devem estar no formato AAAA-MM-DD.",
                    ft.Colors.RED,
                )
                return
            
            # Coletar itens
            for item_container in self.items_list.controls:
                item_fields = item_container.content.controls
                descricao = item_fields[1].value
                quantidade = int(item_fields[2].controls[0].value or 0)
                valor = float(item_fields[2].controls[1].value or 0)
                
                if descricao:
                    ata_data['items'].append({
                        'descricao': descricao,
                        'quantidade': quantidade,
                        'valor': valor
                    })
            
            # Salvar no banco
            if self.current_edit_ata:
                database.update_ata(self.current_edit_ata, ata_data)
            else:
                database.insert_ata(ata_data)
            
            # Atualizar interface
            self.load_atas()
            self.close_modal()
            
            # Mostrar mensagem de sucesso
            self.show_snackbar("Ata salva com sucesso!", ft.Colors.GREEN)
            
        except Exception as ex:
            self.show_snackbar(f"Erro ao salvar ata: {str(ex)}", ft.Colors.RED)

    def edit_ata(self, ata_id: int):
        """Edita uma ata existente."""
        ata = next((a for a in self.atas if a['id'] == ata_id), None)
        if ata:
            self.current_edit_ata = ata_id
            self.populate_modal_fields(ata)
            self.modal.open = True
            self.page.update()

    def populate_modal_fields(self, ata: Dict[str, Any]):
        """Preenche os campos do modal com dados de uma ata."""
        self.numero_ata_field.value = ata['numeroAta']
        self.documento_sei_field.value = ata['documentoSei']
        self.objeto_field.value = ata['objeto']
        self.data_assinatura_field.value = ata['dataAssinatura']
        self.data_vigencia_field.value = ata['dataVigencia']
        self.fornecedor_field.value = ata['fornecedor']
        
        # Telefones
        self.telefones_list.controls.clear()
        for telefone in ata.get('telefonesFornecedor', []):
            self.add_telefone_field()
            self.telefones_list.controls[-1].controls[0].value = telefone
        
        # E-mails
        self.emails_list.controls.clear()
        for email in ata.get('emailsFornecedor', []):
            self.add_email_field()
            self.emails_list.controls[-1].controls[0].value = email
        
        # Itens
        self.items_list.controls.clear()
        for item in ata.get('items', []):
            self.add_item_field()
            item_container = self.items_list.controls[-1]
            item_fields = item_container.content.controls
            item_fields[1].value = item['descricao']
            item_fields[2].controls[0].value = str(item['quantidade'])
            item_fields[2].controls[1].value = str(item['valor'])

    def delete_ata(self, ata_id: int):
        """Deleta uma ata."""
        def confirm_delete(e):
            database.delete_ata(ata_id)
            self.load_atas()
            self.show_snackbar("Ata excluída com sucesso!", ft.Colors.GREEN)
            confirm_dialog.open = False
            self.page.update()

        def cancel_delete(e):
            confirm_dialog.open = False
            self.page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Tem certeza que deseja excluir esta ata? Esta ação não pode ser desfeita."),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete),
                ft.TextButton("Excluir", on_click=confirm_delete, style=ft.ButtonStyle(color=self.colors['status_expired']))
            ]
        )
        
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def show_snackbar(self, message: str, color: str):
        """Mostra uma mensagem de notificação."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()

def main(page: ft.Page):
    app = AtaApp(page)

if __name__ == "__main__":
    ft.app(target=main)

