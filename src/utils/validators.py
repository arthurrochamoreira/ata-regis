import re
from datetime import date, datetime
from typing import List, Optional

class Validators:
    """Classe com métodos de validação"""
    
    @staticmethod
    def validar_numero_ata(numero: str) -> bool:
        """Valida o formato do número da ata (XXXX/AAAA)"""
        return bool(re.match(r'^\d{4}/\d{4}$', numero))
    
    @staticmethod
    def validar_documento_sei(documento: str) -> bool:
        """Valida o formato do documento SEI (00000.000000/0000-00)"""
        return bool(re.match(r'^\d{5}\.\d{6}/\d{4}-\d{2}$', documento))
    
    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        """Valida o formato do telefone (XX) XXXXX-XXXX"""
        return bool(re.match(r'^\(\d{2}\)\s?\d{4,5}-\d{4}$', telefone))
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida o formato do email"""
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    @staticmethod
    def validar_data_vigencia(data_str: str) -> Optional[date]:
        """Valida e converte string de data para objeto date"""
        try:
            return datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            try:
                return datetime.strptime(data_str, "%d/%m/%Y").date()
            except ValueError:
                return None
    
    @staticmethod
    def formatar_telefone(telefone: str) -> str:
        """Formata telefone removendo caracteres especiais e aplicando máscara"""
        # Remove tudo que não é dígito
        digitos = re.sub(r'\D', '', telefone)
        
        # Aplica máscara baseada no número de dígitos
        if len(digitos) == 10:  # Telefone fixo
            return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
        elif len(digitos) == 11:  # Celular
            return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
        else:
            return telefone  # Retorna original se não conseguir formatar
    
    @staticmethod
    def formatar_documento_sei(documento: str) -> str:
        """Formata documento SEI removendo caracteres especiais e aplicando máscara"""
        # Remove tudo que não é dígito
        digitos = re.sub(r'\D', '', documento)
        
        # Aplica máscara se tiver 17 dígitos
        if len(digitos) == 17:
            return f"{digitos[:5]}.{digitos[5:11]}/{digitos[11:15]}-{digitos[15:]}"
        else:
            return documento  # Retorna original se não conseguir formatar
    
    @staticmethod
    def validar_valor_positivo(valor: str) -> Optional[float]:
        """Valida e converte string de valor para float positivo"""
        try:
            # Remove caracteres de formatação
            valor_limpo = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
            valor_float = float(valor_limpo)
            
            if valor_float > 0:
                return valor_float
            else:
                return None
        except ValueError:
            return None
    
    @staticmethod
    def validar_quantidade_positiva(quantidade: str) -> Optional[int]:
        """Valida e converte string de quantidade para int positivo"""
        try:
            quantidade_int = int(quantidade)
            if quantidade_int > 0:
                return quantidade_int
            else:
                return None
        except ValueError:
            return None

class Formatters:
    """Classe com métodos de formatação"""
    
    @staticmethod
    def formatar_data_brasileira(data: date) -> str:
        """Formata data para padrão brasileiro (DD/MM/AAAA)"""
        return data.strftime("%d/%m/%Y")
    
    @staticmethod
    def formatar_valor_monetario(valor: float) -> str:
        """Formata valor para padrão monetário brasileiro"""
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    @staticmethod
    def formatar_status(status: str) -> str:
        """Formata status com ícone"""
        status_map = {
            "vigente": "✅ Vigente",
            "a_vencer": "⚠️ A Vencer",
            "vencida": "❌ Vencida"
        }
        return status_map.get(status, status.title())
    
    @staticmethod
    def formatar_dias_restantes(dias: int) -> str:
        """Formata dias restantes com texto apropriado"""
        if dias < 0:
            return f"Vencida há {abs(dias)} dias"
        elif dias == 0:
            return "Vence hoje"
        elif dias == 1:
            return "Vence amanhã"
        else:
            return f"Faltam {dias} dias"

class MaskUtils:
    """Utilitários para aplicação de máscaras em campos de entrada"""
    
    @staticmethod
    def aplicar_mascara_sei(texto: str) -> str:
        """Aplica máscara ao documento SEI conforme o usuário digita"""
        # Remove tudo que não é dígito
        digitos = re.sub(r'\D', '', texto)
        
        # Aplica máscara progressivamente
        if len(digitos) <= 5:
            return digitos
        elif len(digitos) <= 11:
            return f"{digitos[:5]}.{digitos[5:]}"
        elif len(digitos) <= 15:
            return f"{digitos[:5]}.{digitos[5:11]}/{digitos[11:]}"
        elif len(digitos) <= 17:
            return f"{digitos[:5]}.{digitos[5:11]}/{digitos[11:15]}-{digitos[15:]}"
        else:
            # Limita a 17 dígitos
            digitos = digitos[:17]
            return f"{digitos[:5]}.{digitos[5:11]}/{digitos[11:15]}-{digitos[15:]}"
    
    @staticmethod
    def aplicar_mascara_telefone(texto: str) -> str:
        """Aplica máscara ao telefone conforme o usuário digita"""
        # Remove tudo que não é dígito
        digitos = re.sub(r'\D', '', texto)
        
        # Aplica máscara progressivamente
        if len(digitos) <= 2:
            return f"({digitos}"
        elif len(digitos) <= 6:
            return f"({digitos[:2]}) {digitos[2:]}"
        elif len(digitos) <= 10:
            return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
        elif len(digitos) <= 11:
            return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
        else:
            # Limita a 11 dígitos
            digitos = digitos[:11]
            return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
    
    @staticmethod
    def aplicar_mascara_numero_ata(texto: str) -> str:
        """Aplica máscara ao número da ata conforme o usuário digita"""
        # Remove tudo que não é dígito
        digitos = re.sub(r'\D', '', texto)
        
        # Aplica máscara progressivamente
        if len(digitos) <= 4:
            return digitos
        elif len(digitos) <= 8:
            return f"{digitos[:4]}/{digitos[4:]}"
        else:
            # Limita a 8 dígitos
            digitos = digitos[:8]
            return f"{digitos[:4]}/{digitos[4:]}"

