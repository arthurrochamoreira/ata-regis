import flet as ft
from datetime import date, datetime
from typing import List, Dict, Any, Optional, Callable

try:
    from ..ui.tokens import SPACE_2, SPACE_3, SPACE_4, SPACE_5
except Exception:  # pragma: no cover
    from ui.tokens import SPACE_2, SPACE_3, SPACE_4, SPACE_5
try:
    from ..models.ata import Ata, Item
    from ..utils.validators import Validators, Formatters, MaskUtils
except ImportError:  # Execução direta sem pacote
    from models.ata import Ata, Item
    from utils.validators import Validators, Formatters, MaskUtils

class AtaForm:
    """Formulário para criação e edição de atas"""
    
    def __init__(self, page: ft.Page, on_save: Callable[[Dict[str, Any]], None], 
                 on_cancel: Callable[[], None], ata: Optional[Ata] = None):
        self.page = page
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.ata = ata
        self.is_edit_mode = ata is not None
        
        # Campos do formulário
        self.numero_ata_field = None
        self.numero_ata_value = ""
        self.documento_sei_field = None
        self.data_vigencia_field = None
        self.objeto_field = None
        self.fornecedor_field = None
        self.telefones_container = None
        self.emails_container = None
        self.itens_container = None
        
        # Listas dinâmicas
        self.telefones = []
        self.emails = []
        self.itens = []

        self.build_form()

    def create_textfield(self, label: str, hint: str = "", **kwargs) -> ft.TextField:
        """Retorna um ``TextField`` com estilo padrao."""
        return ft.TextField(
            label=label,
            hint_text=hint,
            label_style=ft.TextStyle(
                color="#4B5563",
                size=12,
                weight=ft.FontWeight.W_500,
            ),
            bgcolor="#FFFFFF",
            content_padding=ft.padding.symmetric(horizontal=12, vertical=14),
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            border_color="#9CA3AF",
            focused_border_color="#3B82F6",
            **kwargs,
        )
    
    def build_form(self):
        """Constrói o formulário seguindo o layout moderno."""
        titulo = "Editar Ata" if self.is_edit_mode else "Nova Ata"

        # Campos
        if self.is_edit_mode and self.ata:
            self.numero_ata_value = self.ata.numero_ata
            numero_ata_control = ft.Column(
                spacing=4,
                controls=[
                    ft.Text(
                        "Número da Ata",
                        size=12,
                        color="#6B7280",
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Container(
                        content=ft.Text(self.numero_ata_value, color="#374151"),
                        bgcolor="#E5E7EB",
                        padding=14,
                        border_radius=8,
                        border=ft.border.all(1, "#D1D5DB"),
                    ),
                ],
            )
        else:
            self.numero_ata_field = self.create_textfield(
                "Número da Ata",
                "0000/0000",
                on_change=self.on_numero_ata_change,
            )
            numero_ata_control = self.numero_ata_field

        self.documento_sei_field = self.create_textfield(
            "Documento SEI",
            "00000.000000/0000-00",
            on_change=self.on_documento_sei_change,
        )
        self.data_vigencia_field = self.create_textfield("Data de Vigência", "DD/MM/AAAA")
        self.objeto_field = self.create_textfield(
            "Objeto",
            "Descrição do objeto da ata",
            multiline=True,
            max_lines=3,
        )
        self.fornecedor_field = self.create_textfield("Fornecedor", "Nome da empresa fornecedora")

        # Containers dinâmicos
        self.telefones_container = ft.Column(spacing=8)
        self.emails_container = ft.Column(spacing=8)
        self.itens_container = ft.Column(spacing=8)

        if self.is_edit_mode:
            self.populate_fields()
        else:
            self.add_telefone()
            self.add_email()
            self.add_item()

        dados_grid = ft.GridView(
            runs_count=2,
            max_extent=400,
            spacing=24,
            controls=[
                numero_ata_control,
                self.documento_sei_field,
                self.data_vigencia_field,
                self.fornecedor_field,
            ],
        )

        dados_gerais = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.icons.DESCRIPTION_OUTLINED, color="#4F46E5"),
                                bgcolor="#E0E7FF",
                                padding=6,
                                border_radius=8,
                            ),
                            ft.Text(
                                "Dados Gerais",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#1F2937",
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    dados_grid,
                    self.objeto_field,
                ],
                spacing=24,
            ),
            bgcolor="#F8FAFC",
            padding=24,
            border_radius=12,
        )

        telefones_section = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.icons.PHONE_OUTLINED, color="#14B8A6"),
                                bgcolor="#CCFBF1",
                                padding=6,
                                border_radius=8,
                            ),
                            ft.Text(
                                "Telefones",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#1F2937",
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    self.telefones_container,
                    ft.TextButton(
                        text="Adicionar telefone",
                        icon=ft.icons.ADD_CIRCLE_OUTLINE,
                        style=ft.ButtonStyle(color="#3B82F6"),
                        on_click=lambda e: self.add_telefone(),
                    ),
                ],
                spacing=24,
            ),
            bgcolor="#F8FAFC",
            padding=24,
            border_radius=12,
        )

        emails_section = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.icons.EMAIL_OUTLINED, color="#E11D48"),
                                bgcolor="#FFE4E6",
                                padding=6,
                                border_radius=8,
                            ),
                            ft.Text(
                                "E-mails",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#1F2937",
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    self.emails_container,
                    ft.TextButton(
                        text="Adicionar e-mail",
                        icon=ft.icons.ADD_CIRCLE_OUTLINE,
                        style=ft.ButtonStyle(color="#3B82F6"),
                        on_click=lambda e: self.add_email(),
                    ),
                ],
                spacing=24,
            ),
            bgcolor="#F8FAFC",
            padding=24,
            border_radius=12,
        )

        itens_section = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.icons.LIST_ALT_OUTLINED, color="#16A34A"),
                                bgcolor="#D1FAE5",
                                padding=6,
                                border_radius=8,
                            ),
                            ft.Text(
                                "Itens da Ata",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#1F2937",
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    self.itens_container,
                    ft.TextButton(
                        text="Adicionar item",
                        icon=ft.icons.ADD_CIRCLE_OUTLINE,
                        style=ft.ButtonStyle(color="#3B82F6"),
                        on_click=lambda e: self.add_item(),
                    ),
                ],
                spacing=24,
            ),
            bgcolor="#F8FAFC",
            padding=24,
            border_radius=12,
        )

        botoes = ft.Row(
            [
                ft.OutlinedButton(
                    text="Cancelar",
                    on_click=lambda e: self.on_cancel(),
                    style=ft.ButtonStyle(
                        padding=14,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                ft.ElevatedButton(
                    text="Salvar",
                    on_click=self.save_ata,
                    bgcolor="#3B82F6",
                    color="#FFFFFF",
                    style=ft.ButtonStyle(
                        padding=14,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=16,
        )

        card = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    titulo,
                                    size=30,
                                    weight=ft.FontWeight.BOLD,
                                    color="#111827",
                                ),
                                ft.Divider(height=1, color="#E5E7EB"),
                            ],
                            spacing=0,
                        ),
                        margin=ft.margin.only(bottom=32),
                    ),
                    dados_gerais,
                    telefones_section,
                    emails_section,
                    itens_section,
                    botoes,
                ],
                spacing=32,
            ),
            width=896,
            bgcolor="#FFFFFF",
            padding=32,
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                offset=ft.Offset(0, 10),
            ),
        )

        page_container = ft.Container(
            content=ft.Column([card], expand=True),
            padding=32,
            bgcolor="#F1F5F9",
            alignment=ft.alignment.top_center,
        )

        self.dialog = ft.AlertDialog(content=page_container, modal=True)

        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
    
    def populate_fields(self):
        """Preenche os campos com dados da ata existente"""
        if not self.ata:
            return
        if self.is_edit_mode:
            self.numero_ata_value = self.ata.numero_ata
        else:
            self.numero_ata_field.value = self.ata.numero_ata
        self.documento_sei_field.value = self.ata.documento_sei
        self.data_vigencia_field.value = self.ata.data_vigencia.strftime("%d/%m/%Y")
        self.objeto_field.value = self.ata.objeto
        self.fornecedor_field.value = self.ata.fornecedor
        
        # Telefones
        for telefone in self.ata.telefones_fornecedor:
            self.add_telefone(telefone)
        
        # E-mails
        for email in self.ata.emails_fornecedor:
            self.add_email(email)
        
        # Itens
        for item in self.ata.itens:
            self.add_item(item)
    
    def add_telefone(self, valor: str = ""):
        """Adiciona campo de telefone"""
        telefone_field = self.create_textfield(
            label=f"Telefone {len(self.telefones) + 1}",
            hint="(XX) XXXXX-XXXX",
            value=valor,
            on_change=self.on_telefone_change,
            expand=True,
        )

        remove_btn = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color="#9CA3AF",
            tooltip="Remover telefone",
        )

        row = ft.Row(
            [telefone_field, remove_btn],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        remove_btn.on_click = lambda e, field=telefone_field, r=row: self.remove_telefone(field, r)
        self.telefones.append((telefone_field, row))
        self.telefones_container.controls.append(row)
        self.page.update()
    
    def remove_telefone(self, field, row):
        """Remove campo de telefone"""
        self.telefones = [(f, r) for f, r in self.telefones if f != field]
        if row in self.telefones_container.controls:
            self.telefones_container.controls.remove(row)
        self.page.update()
    
    def add_email(self, valor: str = ""):
        """Adiciona campo de e-mail"""
        email_field = self.create_textfield(
            label=f"E-mail {len(self.emails) + 1}",
            hint="email@exemplo.com",
            value=valor,
            expand=True,
        )

        remove_btn = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color="#9CA3AF",
            tooltip="Remover e-mail",
        )

        row = ft.Row(
            [email_field, remove_btn],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        remove_btn.on_click = lambda e, field=email_field, r=row: self.remove_email(field, r)
        self.emails.append((email_field, row))
        self.emails_container.controls.append(row)
        self.page.update()
    
    def remove_email(self, field, row):
        """Remove campo de e-mail"""
        self.emails = [(f, r) for f, r in self.emails if f != field]
        if row in self.emails_container.controls:
            self.emails_container.controls.remove(row)
        self.page.update()
    
    def add_item(self, item: Optional[Item] = None):
        """Adiciona campos de item"""
        descricao_field = self.create_textfield(
            "Descrição",
            "Descrição do item",
            value=item.descricao if item else "",
            expand=True,
        )

        quantidade_field = self.create_textfield(
            "Quantidade",
            "0",
            value=str(item.quantidade) if item else "",
            width=100,
        )

        valor_field = self.create_textfield(
            "Valor Unitário",
            "0,00",
            value=f"{item.valor:.2f}".replace(".", ",") if item else "",
            width=120,
        )

        remove_btn = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color="#9CA3AF",
            tooltip="Remover item",
            on_click=lambda e: self.remove_item(descricao_field, row),
        )

        row = ft.Row(
            [descricao_field, quantidade_field, valor_field, remove_btn],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.itens.append((descricao_field, quantidade_field, valor_field, row))
        self.itens_container.controls.append(row)
        self.page.update()
    
    def remove_item(self, descricao_field, row):
        """Remove campos de item"""
        self.itens = [(d, q, v, r) for d, q, v, r in self.itens if d != descricao_field]
        if row in self.itens_container.controls:
            self.itens_container.controls.remove(row)
        self.page.update()
    
    def on_numero_ata_change(self, e):
        """Aplica máscara ao número da ata"""
        e.control.value = MaskUtils.aplicar_mascara_numero_ata(e.control.value)
        self.page.update()
    
    def on_documento_sei_change(self, e):
        """Aplica máscara ao documento SEI"""
        e.control.value = MaskUtils.aplicar_mascara_sei(e.control.value)
        self.page.update()
    
    def on_telefone_change(self, e):
        """Aplica máscara ao telefone"""
        e.control.value = MaskUtils.aplicar_mascara_telefone(e.control.value)
        self.page.update()
    
    def validate_form(self) -> List[str]:
        """Valida o formulário e retorna lista de erros"""
        erros = []
        
        numero = self.numero_ata_value if self.is_edit_mode else self.numero_ata_field.value
        if not numero:
            erros.append("Número da ata é obrigatório")
        elif not Validators.validar_numero_ata(numero):
            erros.append("Número da ata deve seguir o formato XXXX/AAAA")
        
        # Valida documento SEI
        if not self.documento_sei_field.value:
            erros.append("Documento SEI é obrigatório")
        elif not Validators.validar_documento_sei(self.documento_sei_field.value):
            erros.append("Documento SEI deve seguir o formato 00000.000000/0000-00")
        
        # Valida data de vigência
        if not self.data_vigencia_field.value:
            erros.append("Data de vigência é obrigatória")
        elif not Validators.validar_data_vigencia(self.data_vigencia_field.value):
            erros.append("Data de vigência deve estar no formato DD/MM/AAAA")
        
        # Valida objeto
        if not self.objeto_field.value or not self.objeto_field.value.strip():
            erros.append("Objeto é obrigatório")
        
        # Valida fornecedor
        if not self.fornecedor_field.value or not self.fornecedor_field.value.strip():
            erros.append("Fornecedor é obrigatório")
        
        # Valida telefones
        telefones_validos = []
        for telefone_field, _ in self.telefones:
            if telefone_field.value and telefone_field.value.strip():
                if Validators.validar_telefone(telefone_field.value):
                    telefones_validos.append(telefone_field.value)
                else:
                    erros.append(f"Telefone {telefone_field.value} não é válido")
        
        if not telefones_validos:
            erros.append("Pelo menos um telefone é obrigatório")
        
        # Valida e-mails
        emails_validos = []
        for email_field, _ in self.emails:
            if email_field.value and email_field.value.strip():
                if Validators.validar_email(email_field.value):
                    emails_validos.append(email_field.value)
                else:
                    erros.append(f"E-mail {email_field.value} não é válido")
        
        if not emails_validos:
            erros.append("Pelo menos um e-mail é obrigatório")
        
        # Valida itens
        itens_validos = []
        for desc_field, qtd_field, val_field, _ in self.itens:
            if desc_field.value and desc_field.value.strip():
                quantidade = Validators.validar_quantidade_positiva(qtd_field.value)
                valor = Validators.validar_valor_positivo(val_field.value.replace(",", "."))
                
                if quantidade is None:
                    erros.append(f"Quantidade do item '{desc_field.value}' deve ser um número positivo")
                elif valor is None:
                    erros.append(f"Valor do item '{desc_field.value}' deve ser um número positivo")
                else:
                    itens_validos.append({
                        "descricao": desc_field.value.strip(),
                        "quantidade": quantidade,
                        "valor": valor
                    })
        
        if not itens_validos:
            erros.append("Pelo menos um item é obrigatório")
        
        return erros
    
    def save_ata(self, e):
        """Salva a ata"""
        erros = self.validate_form()
        
        if erros:
            # Mostra erros
            erro_dialog = ft.AlertDialog(
                title=ft.Text("Erros de Validação"),
                content=ft.Column([
                    ft.Text("Corrija os seguintes erros:"),
                    *[ft.Text(f"• {erro}") for erro in erros]
                ], tight=True),
                actions=[ft.TextButton("OK", on_click=lambda e: self.close_error_dialog())]
            )
            self.page.dialog = erro_dialog
            erro_dialog.open = True
            self.page.update()
            return
        
        # Coleta dados do formulário
        data_vigencia = Validators.validar_data_vigencia(self.data_vigencia_field.value)
        
        telefones = [f.value for f, _ in self.telefones if f.value and f.value.strip()]
        emails = [f.value for f, _ in self.emails if f.value and f.value.strip()]
        
        itens = []
        for desc_field, qtd_field, val_field, _ in self.itens:
            if desc_field.value and desc_field.value.strip():
                itens.append({
                    "descricao": desc_field.value.strip(),
                    "quantidade": int(qtd_field.value),
                    "valor": float(val_field.value.replace(",", "."))
                })
        
        numero = self.numero_ata_value if self.is_edit_mode else self.numero_ata_field.value
        ata_data = {
            "numero_ata": numero,
            "documento_sei": self.documento_sei_field.value,
            "data_vigencia": data_vigencia.isoformat(),
            "objeto": self.objeto_field.value.strip(),
            "fornecedor": self.fornecedor_field.value.strip(),
            "telefones_fornecedor": telefones,
            "emails_fornecedor": emails,
            "itens": itens
        }
        
        # Fecha o diálogo
        self.dialog.open = False
        self.page.update()
        
        # Chama callback de salvamento
        self.on_save(ata_data)
    
    def close_error_dialog(self):
        """Fecha o diálogo de erro"""
        self.page.dialog.open = False
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

