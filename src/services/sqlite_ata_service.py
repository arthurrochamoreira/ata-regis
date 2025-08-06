import sqlite3
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from settings import settings

try:
    from ..models.ata import Ata, Item
except ImportError:  # pragma: no cover - support execution without package
    from models.ata import Ata, Item

class SQLiteAtaService:
    """Serviço de Atas usando SQLite como persistência."""

    def __init__(self, db_file: str | None = None):
        self.db_file = db_file or settings.DB_FILE
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        # Garante que chaves estrangeiras executem os comandos ON DELETE CASCADE
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()
        if not self._has_atas():
            self.load_mock_data()

    def _create_tables(self):
        """Cria as tabelas necessárias se não existirem."""
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS atas (
                    numero_ata TEXT PRIMARY KEY,
                    documento_sei TEXT,
                    data_vigencia TEXT,
                    objeto TEXT,
                    fornecedor TEXT
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS itens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_ata TEXT,
                    descricao TEXT,
                    quantidade INTEGER,
                    valor REAL,
                    FOREIGN KEY(numero_ata) REFERENCES atas(numero_ata) ON DELETE CASCADE
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS telefones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_ata TEXT,
                    telefone TEXT,
                    FOREIGN KEY(numero_ata) REFERENCES atas(numero_ata) ON DELETE CASCADE
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_ata TEXT,
                    email TEXT,
                    FOREIGN KEY(numero_ata) REFERENCES atas(numero_ata) ON DELETE CASCADE
                )
                """
            )

    def _has_atas(self) -> bool:
        cur = self.conn.execute("SELECT COUNT(*) FROM atas")
        return cur.fetchone()[0] > 0

    # --------- Conversões ---------
    def _ata_from_db(self, row: sqlite3.Row) -> Ata:
        numero = row["numero_ata"]
        itens_rows = self.conn.execute(
            "SELECT descricao, quantidade, valor FROM itens WHERE numero_ata=?",
            (numero,),
        ).fetchall()
        itens = [Item(descricao=r[0], quantidade=r[1], valor=r[2]) for r in itens_rows]
        telefones = [r[0] for r in self.conn.execute(
            "SELECT telefone FROM telefones WHERE numero_ata=?", (numero,)
        ).fetchall()]
        emails = [r[0] for r in self.conn.execute(
            "SELECT email FROM emails WHERE numero_ata=?", (numero,)
        ).fetchall()]
        data_vigencia = datetime.strptime(row["data_vigencia"], "%Y-%m-%d").date()
        return Ata(
            numero_ata=numero,
            documento_sei=row["documento_sei"],
            data_vigencia=data_vigencia,
            objeto=row["objeto"],
            itens=itens,
            fornecedor=row["fornecedor"],
            telefones_fornecedor=telefones,
            emails_fornecedor=emails,
        )

    # --------- Operações CRUD ---------
    def criar_ata(self, ata_data: Dict[str, Any]) -> Ata:
        if self.buscar_por_numero(ata_data["numero_ata"]):
            raise ValueError(f"Já existe uma ata com o número {ata_data['numero_ata']}")
        ata = Ata.from_dict(ata_data)
        with self.conn:
            self.conn.execute(
                "INSERT INTO atas (numero_ata, documento_sei, data_vigencia, objeto, fornecedor) VALUES (?, ?, ?, ?, ?)",
                (
                    ata.numero_ata,
                    ata.documento_sei,
                    ata.data_vigencia.isoformat(),
                    ata.objeto,
                    ata.fornecedor,
                ),
            )
            for item in ata.itens:
                self.conn.execute(
                    "INSERT INTO itens (numero_ata, descricao, quantidade, valor) VALUES (?, ?, ?, ?)",
                    (
                        ata.numero_ata,
                        item.descricao,
                        item.quantidade,
                        item.valor,
                    ),
                )
            for telefone in ata.telefones_fornecedor:
                self.conn.execute(
                    "INSERT INTO telefones (numero_ata, telefone) VALUES (?, ?)",
                    (ata.numero_ata, telefone),
                )
            for email in ata.emails_fornecedor:
                self.conn.execute(
                    "INSERT INTO emails (numero_ata, email) VALUES (?, ?)",
                    (ata.numero_ata, email),
                )
        return ata

    def editar_ata(self, numero_ata: str, ata_data: Dict[str, Any]) -> Optional[Ata]:
        if not self.buscar_por_numero(numero_ata):
            return None
        self.excluir_ata(numero_ata)
        return self.criar_ata(ata_data)

    def excluir_ata(self, numero_ata: str) -> bool:
        with self.conn:
            cur = self.conn.execute("DELETE FROM atas WHERE numero_ata=?", (numero_ata,))
            return cur.rowcount > 0

    def buscar_por_numero(self, numero_ata: str) -> Optional[Ata]:
        row = self.conn.execute("SELECT * FROM atas WHERE numero_ata=?", (numero_ata,)).fetchone()
        return self._ata_from_db(row) if row else None

    def listar_todas(self) -> List[Ata]:
        rows = self.conn.execute("SELECT * FROM atas").fetchall()
        return [self._ata_from_db(r) for r in rows]

    def filtrar_por_status(self, status: str) -> List[Ata]:
        return [ata for ata in self.listar_todas() if ata.status == status]

    def buscar_por_texto(self, texto: str) -> List[Ata]:
        texto = f"%{texto.lower()}%"
        rows = self.conn.execute(
            """
            SELECT * FROM atas WHERE 
                lower(numero_ata) LIKE ? OR 
                lower(objeto) LIKE ? OR 
                lower(fornecedor) LIKE ? OR 
                lower(documento_sei) LIKE ?
            """,
            (texto, texto, texto, texto),
        ).fetchall()
        return [self._ata_from_db(r) for r in rows]

    def get_estatisticas(self) -> Dict[str, int]:
        stats = {"vigente": 0, "a_vencer": 0, "vencida": 0}
        for ata in self.listar_todas():
            stats[ata.status] += 1
        return stats

    def get_atas_vencimento_proximo(self, dias: int | None = None) -> List[Ata]:
        dias = dias or settings.VENCIMENTO_ALERT_DAYS
        atas = [ata for ata in self.listar_todas() if 0 <= ata.dias_restantes <= dias]
        return sorted(atas, key=lambda x: x.dias_restantes)

    def validar_numero_ata_unico(self, numero_ata: str, excluir_numero: str | None = None) -> bool:
        row = self.conn.execute(
            "SELECT numero_ata FROM atas WHERE numero_ata=?", (numero_ata,)
        ).fetchone()
        if row is None:
            return True
        return row[0] == excluir_numero

    def get_proxima_numeracao(self, ano: int | None = None) -> str:
        if ano is None:
            ano = date.today().year
        pattern = f"/%{ano}"
        rows = self.conn.execute(
            "SELECT numero_ata FROM atas WHERE numero_ata LIKE ?", (pattern,)
        ).fetchall()
        maior = 0
        for r in rows:
            try:
                numero = int(r[0].split("/")[0])
                if numero > maior:
                    maior = numero
            except ValueError:
                continue
        return f"{maior+1:04d}/{ano}"

    # --------- Mock data ---------
    def load_mock_data(self):
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
                "emails_fornecedor": ["contato@empresa.com"],
            },
            {
                "numero_ata": "0015/2024",
                "documento_sei": "23106.033566/2023-29",
                "data_vigencia": "2024-08-15",
                "objeto": "Material de Escritório",
                "itens": [
                    {"descricao": "Papel A4", "quantidade": 100, "valor": 25.00},
                    {"descricao": "Canetas", "quantidade": 50, "valor": 2.50},
                ],
                "fornecedor": "Papelaria ABC",
                "telefones_fornecedor": ["(61) 88888-1111"],
                "emails_fornecedor": ["vendas@papelaria.com"],
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
                "emails_fornecedor": ["tech@techcorp.com"],
            },
        ]
        for ata in mock_data:
            self.criar_ata(ata)

    def close(self):
        if self.conn:
            self.conn.close()
