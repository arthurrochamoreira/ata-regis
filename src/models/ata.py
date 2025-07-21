from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import date, datetime
import re

@dataclass
class Item:
    """Representa um item da ata"""
    descricao: str
    quantidade: int
    valor: float
    
    def __post_init__(self):
        """Validações após inicialização"""
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        if self.valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
        if not self.descricao.strip():
            raise ValueError("Descrição não pode estar vazia")
    
    @property
    def valor_total(self) -> float:
        """Calcula o valor total do item"""
        return self.quantidade * self.valor
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "descricao": self.descricao,
            "quantidade": self.quantidade,
            "valor": self.valor
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """Cria instância a partir de dicionário"""
        return cls(
            descricao=data["descricao"],
            quantidade=data["quantidade"],
            valor=data["valor"]
        )

@dataclass
class Ata:
    """Representa uma Ata de Registro de Preços"""
    numero_ata: str
    documento_sei: str
    data_vigencia: date
    objeto: str
    itens: List[Item] = field(default_factory=list)
    fornecedor: str = ""
    telefones_fornecedor: List[str] = field(default_factory=list)
    emails_fornecedor: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validações após inicialização"""
        self.validate()
    
    def validate(self):
        """Valida todos os campos da ata"""
        self._validate_numero_ata()
        self._validate_documento_sei()
        self._validate_data_vigencia()
        self._validate_objeto()
        self._validate_fornecedor()
        self._validate_telefones()
        self._validate_emails()
        self._validate_itens()
    
    def _validate_numero_ata(self):
        """Valida o formato do número da ata (XXXX/AAAA)"""
        if not re.match(r'^\d{4}/\d{4}$', self.numero_ata):
            raise ValueError("Número da ata deve seguir o formato XXXX/AAAA")
    
    def _validate_documento_sei(self):
        """Valida o formato do documento SEI (00000.000000/0000-00)"""
        if not re.match(r'^\d{5}\.\d{6}/\d{4}-\d{2}$', self.documento_sei):
            raise ValueError("Documento SEI deve seguir o formato 00000.000000/0000-00")
    
    def _validate_data_vigencia(self):
        """Valida a data de vigência"""
        if not isinstance(self.data_vigencia, date):
            raise ValueError("Data de vigência deve ser do tipo date")
        
        # Converte string para date se necessário
        if isinstance(self.data_vigencia, str):
            try:
                self.data_vigencia = datetime.strptime(self.data_vigencia, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Data de vigência deve estar no formato YYYY-MM-DD")
    
    def _validate_objeto(self):
        """Valida o objeto da ata"""
        if not self.objeto.strip():
            raise ValueError("Objeto não pode estar vazio")
    
    def _validate_fornecedor(self):
        """Valida o fornecedor"""
        if not self.fornecedor.strip():
            raise ValueError("Fornecedor não pode estar vazio")
    
    def _validate_telefones(self):
        """Valida os telefones do fornecedor"""
        telefone_pattern = r'^\(\d{2}\)\s?\d{4,5}-\d{4}$'
        for telefone in self.telefones_fornecedor:
            if not re.match(telefone_pattern, telefone):
                raise ValueError(f"Telefone {telefone} deve seguir o formato (XX) XXXXX-XXXX")
    
    def _validate_emails(self):
        """Valida os emails do fornecedor"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for email in self.emails_fornecedor:
            if not re.match(email_pattern, email):
                raise ValueError(f"Email {email} não é válido")
    
    def _validate_itens(self):
        """Valida os itens da ata"""
        if not self.itens:
            raise ValueError("Ata deve ter pelo menos um item")
        
        for item in self.itens:
            if not isinstance(item, Item):
                raise ValueError("Todos os itens devem ser instâncias da classe Item")
    
    @property
    def valor_total(self) -> float:
        """Calcula o valor total da ata"""
        return sum(item.valor_total for item in self.itens)
    
    @property
    def status(self) -> str:
        """Retorna o status da ata baseado na data de vigência"""
        hoje = date.today()
        dias_restantes = (self.data_vigencia - hoje).days
        
        if dias_restantes < 0:
            return "vencida"
        elif dias_restantes <= 90:
            return "a_vencer"
        else:
            return "vigente"
    
    @property
    def dias_restantes(self) -> int:
        """Retorna os dias restantes para vencimento"""
        hoje = date.today()
        return (self.data_vigencia - hoje).days
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "numero_ata": self.numero_ata,
            "documento_sei": self.documento_sei,
            "data_vigencia": self.data_vigencia.isoformat(),
            "objeto": self.objeto,
            "itens": [item.to_dict() for item in self.itens],
            "fornecedor": self.fornecedor,
            "telefones_fornecedor": self.telefones_fornecedor,
            "emails_fornecedor": self.emails_fornecedor
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ata':
        """Cria instância a partir de dicionário"""
        # Converte string de data para objeto date
        if isinstance(data["data_vigencia"], str):
            data_vigencia = datetime.strptime(data["data_vigencia"], "%Y-%m-%d").date()
        else:
            data_vigencia = data["data_vigencia"]
        
        # Converte itens
        itens = [Item.from_dict(item_data) for item_data in data.get("itens", [])]
        
        return cls(
            numero_ata=data["numero_ata"],
            documento_sei=data["documento_sei"],
            data_vigencia=data_vigencia,
            objeto=data["objeto"],
            itens=itens,
            fornecedor=data.get("fornecedor", ""),
            telefones_fornecedor=data.get("telefones_fornecedor", []),
            emails_fornecedor=data.get("emails_fornecedor", [])
        )
    
    def __str__(self) -> str:
        """Representação em string"""
        return f"Ata {self.numero_ata} - {self.objeto} ({self.status})"

