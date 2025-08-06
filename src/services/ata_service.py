import json
import os
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from settings import settings

# Importações condicionais para suportar execução direta e como módulo
try:
    from ..models.ata import Ata, Item
except ImportError:
    from models.ata import Ata, Item

class AtaService:
    """Serviço para gerenciar operações CRUD das atas"""
    
    def __init__(self, data_file: str | None = None):
        self.data_file = data_file or settings.JSON_DATA_FILE
        self.atas: List[Ata] = []
        self.load_data()
    
    def load_data(self):
        """Carrega dados do arquivo JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.atas = [Ata.from_dict(ata_data) for ata_data in data]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Erro ao carregar dados: {e}")
                self.load_mock_data()
        else:
            self.load_mock_data()
    
    def save_data(self):
        """Salva dados no arquivo JSON"""
        try:
            data = [ata.to_dict() for ata in self.atas]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def load_mock_data(self):
        """Carrega dados mockados para teste"""
        mock_data = [
            {
                "numero_ata": "0016/2024",
                "documento_sei": "23106.033566/2023-30",
                "data_vigencia": "2024-12-31",
                "objeto": "Micro Tipo I",
                "itens": [
                    {"descricao": "Notebook com SSD", "quantidade": 15, "valor": 3500.00}
                ],
                "fornecedor": "Empresa XYZ Ltda",
                "telefones_fornecedor": ["(61) 99999-0000"],
                "emails_fornecedor": ["contato@empresa.com"]
            },
            {
                "numero_ata": "0015/2024",
                "documento_sei": "23106.033566/2023-29",
                "data_vigencia": "2024-08-15",
                "objeto": "Material de Escritório",
                "itens": [
                    {"descricao": "Papel A4", "quantidade": 100, "valor": 25.00},
                    {"descricao": "Canetas", "quantidade": 50, "valor": 2.50}
                ],
                "fornecedor": "Papelaria ABC",
                "telefones_fornecedor": ["(61) 88888-1111"],
                "emails_fornecedor": ["vendas@papelaria.com"]
            },
            {
                "numero_ata": "0014/2024",
                "documento_sei": "23106.033566/2023-28",
                "data_vigencia": "2023-12-31",
                "objeto": "Equipamentos de TI",
                "itens": [
                    {"descricao": "Monitor 24 polegadas", "quantidade": 20, "valor": 800.00}
                ],
                "fornecedor": "TechCorp Ltda",
                "telefones_fornecedor": ["(61) 77777-2222"],
                "emails_fornecedor": ["tech@techcorp.com"]
            }
        ]
        
        try:
            self.atas = [Ata.from_dict(ata_data) for ata_data in mock_data]
            self.save_data()  # Salva os dados mockados
        except Exception as e:
            print(f"Erro ao carregar dados mockados: {e}")
            self.atas = []
    
    def criar_ata(self, ata_data: Dict[str, Any]) -> Ata:
        """Cria uma nova ata"""
        # Verifica se já existe ata com o mesmo número
        if self.buscar_por_numero(ata_data["numero_ata"]):
            raise ValueError(f"Já existe uma ata com o número {ata_data['numero_ata']}")
        
        ata = Ata.from_dict(ata_data)
        self.atas.append(ata)
        self.save_data()
        return ata
    
    def editar_ata(self, numero_ata: str, ata_data: Dict[str, Any]) -> Optional[Ata]:
        """Edita uma ata existente"""
        ata = self.buscar_por_numero(numero_ata)
        if not ata:
            return None
        
        # Remove a ata antiga
        self.atas.remove(ata)
        
        # Cria a ata atualizada
        ata_atualizada = Ata.from_dict(ata_data)
        self.atas.append(ata_atualizada)
        self.save_data()
        return ata_atualizada
    
    def excluir_ata(self, numero_ata: str) -> bool:
        """Exclui uma ata"""
        ata = self.buscar_por_numero(numero_ata)
        if not ata:
            return False
        
        self.atas.remove(ata)
        self.save_data()
        return True
    
    def buscar_por_numero(self, numero_ata: str) -> Optional[Ata]:
        """Busca uma ata pelo número"""
        for ata in self.atas:
            if ata.numero_ata == numero_ata:
                return ata
        return None
    
    def listar_todas(self) -> List[Ata]:
        """Lista todas as atas"""
        return self.atas.copy()
    
    def filtrar_por_status(self, status: str) -> List[Ata]:
        """Filtra atas por status"""
        return [ata for ata in self.atas if ata.status == status]
    
    def buscar_por_texto(self, texto: str) -> List[Ata]:
        """Busca atas por texto (número, objeto, fornecedor)"""
        texto = texto.lower()
        resultado = []
        
        for ata in self.atas:
            if (texto in ata.numero_ata.lower() or
                texto in ata.objeto.lower() or
                texto in ata.fornecedor.lower() or
                texto in ata.documento_sei.lower()):
                resultado.append(ata)
        
        return resultado
    
    def get_estatisticas(self) -> Dict[str, int]:
        """Retorna estatísticas das atas por status"""
        stats = {"vigente": 0, "a_vencer": 0, "vencida": 0}
        for ata in self.atas:
            stats[ata.status] += 1
        return stats
    
    def get_atas_vencimento_proximo(self, dias: int = 90) -> List[Ata]:
        """Retorna atas próximas do vencimento"""
        resultado = []
        for ata in self.atas:
            if 0 <= ata.dias_restantes <= dias:
                resultado.append(ata)
        
        # Ordena por dias restantes
        resultado.sort(key=lambda x: x.dias_restantes)
        return resultado
    
    def validar_numero_ata_unico(self, numero_ata: str, excluir_numero: str = None) -> bool:
        """Valida se o número da ata é único"""
        for ata in self.atas:
            if ata.numero_ata == numero_ata and ata.numero_ata != excluir_numero:
                return False
        return True
    
    def get_proxima_numeracao(self, ano: int = None) -> str:
        """Sugere a próxima numeração para uma ata"""
        if ano is None:
            ano = date.today().year
        
        # Busca o maior número do ano
        maior_numero = 0
        for ata in self.atas:
            if f"/{ano}" in ata.numero_ata:
                try:
                    numero = int(ata.numero_ata.split("/")[0])
                    if numero > maior_numero:
                        maior_numero = numero
                except ValueError:
                    continue
        
        proximo_numero = maior_numero + 1
        return f"{proximo_numero:04d}/{ano}"

