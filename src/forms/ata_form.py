import flet as ft
from datetime import date, datetime
from typing import List, Dict, Any, Optional, Callable

from theme.tokens import TOKENS as T

C, S, R, SH = T.colors, T.spacing, T.radius, T.shadows
from components import PrimaryButton, SecondaryButton, TextInput, IconAction
from ui.tokens import build_section
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
    
    def build_form(self):
        """Constrói o formulário"""
        # Título
        titulo = "Editar Ata" if self.is_edit_mode else "Nova Ata"
        
        # Campos básicos
        self.numero_ata_field = TextInput(
            label="Número da Ata",
            hint_text="0000/0000",
            on_change=self.on_numero_ata_change,
            expand=True,
            border_radius=R.RADIUS_FULL,
        )

        self.documento_sei_field = TextInput(
            label="Documento SEI",
            hint_text="00000.000000/0000-00",
            on_change=self.on_documento_sei_change,
            expand=True,
            border_radius=R.RADIUS_FULL,
        )

        self.data_vigencia_field = TextInput(
            label="Data de Vigência",
            hint_text="DD/MM/AAAA",
            expand=True,
            border_radius=R.RADIUS_FULL,
        )

        self.objeto_field = TextInput(
            label="Objeto",
            hint_text="Descrição do objeto da ata",
            multiline=True,
            max_lines=3,
            expand=True,
            border_radius=R.RADIUS_FULL,
        )

        self.fornecedor_field = TextInput(
            label="Fornecedor",
            hint_text="Nome da empresa fornecedora",
            expand=True,
            border_radius=R.RADIUS_FULL,
        )
        
        # Containers para listas dinâmicas
        self.telefones_container = ft.Column(spacing=S.SPACE_2)
        self.emails_container = ft.Column(spacing=S.SPACE_2)
        self.itens_container = ft.Column(spacing=S.SPACE_2)
        
        # Preenche campos se estiver editando
        if self.is_edit_mode:
            self.populate_fields()
        else:
            # Adiciona campos vazios para nova ata
            self.add_telefone()
            self.add_email()
            self.add_item()
        
        # Seções do formulário
        self.numero_ata_field.col = {"xs": 12, "md": 6}
        self.documento_sei_field.col = {"xs": 12, "md": 6}
        self.data_vigencia_field.col = {"xs": 12, "md": 6}
        self.objeto_field.col = {"xs": 12, "md": 6}
        self.fornecedor_field.col = {"xs": 12, "md": 6}
        dados_gerais_body = ft.ResponsiveRow(
            [
                self.numero_ata_field,
                self.documento_sei_field,
                self.data_vigencia_field,
                self.objeto_field,
                self.fornecedor_field,
            ],
            columns=12,
            spacing=S.SPACE_4,
            run_spacing=S.SPACE_4,
        )
        dados_gerais = build_section(
            "Dados Gerais",
            ft.icons.DESCRIPTION_OUTLINED,
            C.INDIGO,
            C.INDIGO_BG,
            dados_gerais_body,
        )
        
        telefones_header_btn = IconAction(
            icon=ft.icons.ADD,
            tooltip="Adicionar telefone",
            on_click=lambda e: self.add_telefone(),
            hover_color=T.colors.BLUE_HOVER,
            size="sm",
        )
        telefones_section = build_section(
            "Telefones",
            ft.icons.PHONE_OUTLINED,
            C.TEXT_SECONDARY,
            C.GREY_LIGHT,
            ft.Column([
                ft.Row([
                    telefones_header_btn
                ], alignment=ft.MainAxisAlignment.END),
                self.telefones_container,
            ], spacing=S.SPACE_2),
        )
        
        emails_header_btn = IconAction(
            icon=ft.icons.ADD,
            tooltip="Adicionar e-mail",
            on_click=lambda e: self.add_email(),
            hover_color=T.colors.BLUE_HOVER,
            size="sm",
        )
        emails_section = build_section(
            "E-mails",
            ft.icons.EMAIL_OUTLINED,
            C.TEXT_SECONDARY,
            C.GREY_LIGHT,
            ft.Column([
                ft.Row([
                    emails_header_btn
                ], alignment=ft.MainAxisAlignment.END),
                self.emails_container,
            ], spacing=S.SPACE_2),
        )
        
        itens_header_btn = IconAction(
            icon=ft.icons.ADD,
            tooltip="Adicionar item",
            on_click=lambda e: self.add_item(),
            hover_color=T.colors.BLUE_HOVER,
            size="sm",
        )
        itens_section = build_section(
            "Itens",
            ft.icons.LIST_ALT_OUTLINED,
            C.INDIGO,
            C.INDIGO_BG,
            ft.Column([
                ft.Row([
                    itens_header_btn
                ], alignment=ft.MainAxisAlignment.END),
                self.itens_container,
            ], spacing=S.SPACE_2),
        )
        
        # Botões responsivos: ocupam toda a largura em telas pequenas
        botoes = ft.ResponsiveRow(
            [
                SecondaryButton(
                    "Cancelar",
                    on_click=lambda e: self.on_cancel(),
                    expand=True,
                    col={"xs": 12, "md": 6},
                ),
                PrimaryButton(
                    "Salvar",
                    on_click=self.save_ata,
                    expand=True,
                    col={"xs": 12, "md": 6},
                ),
            ],
            columns=12,
            spacing=S.SPACE_4,
            run_spacing=S.SPACE_4,
            alignment=ft.MainAxisAlignment.END,
        )
        
        header = ft.Row(
            [
                ft.Column(
                    spacing=S.SPACE_1,
                    controls=[
                        ft.Text(
                            "Ata de Registro de Preços",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=C.TEXT_DARK,
                        ),
                        ft.Text(titulo, size=16, color=C.TEXT_SECONDARY),
                    ],
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        content = ft.Column(
            [dados_gerais, telefones_section, emails_section, itens_section, botoes],
            spacing=S.SPACE_5,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        card = ft.Container(
            content=ft.Column([header, content], spacing=S.SPACE_6, expand=True),
            bgcolor=C.WHITE,
            padding=ft.padding.only(
                left=S.SPACE_5,
                right=S.SPACE_5,
                top=S.SPACE_4,
                bottom=S.SPACE_4,
            ),
            border_radius=R.RADIUS_MD,
            alignment=ft.alignment.center,
            shadow=SH.SHADOW_LG,
            expand=True,
            width=1152,
        )

        self.dialog = ft.AlertDialog(content=card, modal=True)
        
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
    
    def populate_fields(self):
        """Preenche os campos com dados da ata existente"""
        if not self.ata:
            return
        
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
        telefone_field = TextInput(
            label=f"Telefone {len(self.telefones) + 1}",
            hint_text="(XX) XXXXX-XXXX",
            value=valor,
            on_change=self.on_telefone_change,
            border_radius=R.RADIUS_FULL,
            expand=True,
            col={"xs": 10, "md": 11},
        )

        remove_btn = IconAction(
            icon=ft.icons.DELETE,
            tooltip="Remover telefone",
            on_click=None,
            hover_color=T.colors.RED,
            size="sm",
            col={"xs": 2, "md": 1},
        )

        row = ft.ResponsiveRow(
            [telefone_field, remove_btn],
            columns=12,
            spacing=S.SPACE_2,
            run_spacing=S.SPACE_2,
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
        email_field = TextInput(
            label=f"E-mail {len(self.emails) + 1}",
            hint_text="email@exemplo.com",
            value=valor,
            border_radius=R.RADIUS_FULL,
            expand=True,
            col={"xs": 10, "md": 11},
        )

        remove_btn = IconAction(
            icon=ft.icons.DELETE,
            tooltip="Remover e-mail",
            on_click=None,
            hover_color=T.colors.RED,
            size="sm",
            col={"xs": 2, "md": 1},
        )

        row = ft.ResponsiveRow(
            [email_field, remove_btn],
            columns=12,
            spacing=S.SPACE_2,
            run_spacing=S.SPACE_2,
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
        descricao_field = TextInput(
            label="Descrição",
            hint_text="Descrição do item",
            value=item.descricao if item else "",
            border_radius=R.RADIUS_FULL,
            expand=True,
            col={"xs": 12, "md": 5},
        )

        quantidade_field = TextInput(
            label="Quantidade",
            hint_text="0",
            value=str(item.quantidade) if item else "",
            border_radius=R.RADIUS_FULL,
            expand=True,
            col={"xs": 12, "md": 2},
        )

        valor_field = TextInput(
            label="Valor Unitário",
            hint_text="0,00",
            value=f"{item.valor:.2f}".replace(".", ",") if item else "",
            border_radius=R.RADIUS_FULL,
            expand=True,
            col={"xs": 12, "md": 3},
        )

        remove_btn = IconAction(
            icon=ft.icons.DELETE,
            tooltip="Remover item",
            on_click=None,
            hover_color=T.colors.RED,
            size="sm",
            col={"xs": 12, "md": 2},
        )

        row = ft.ResponsiveRow(
            [
                descricao_field,
                quantidade_field,
                valor_field,
                remove_btn,
            ],
            columns=12,
            spacing=S.SPACE_2,
            run_spacing=S.SPACE_2,
        )

        remove_btn.on_click = lambda e: self.remove_item(descricao_field, row)

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
        
        # Valida número da ata
        if not self.numero_ata_field.value:
            erros.append("Número da ata é obrigatório")
        elif not Validators.validar_numero_ata(self.numero_ata_field.value):
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
        
        ata_data = {
            "numero_ata": self.numero_ata_field.value,
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

