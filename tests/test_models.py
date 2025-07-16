import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from datetime import datetime
import database


def test_create_ata(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_NAME", str(db_path))
    database.create_tables()

    ata_data = {
        "numeroAta": "0001/2024",
        "documentoSei": "21482502",
        "objeto": "Micro Tipo I",
        "dataAssinatura": "2024-01-01",
        "dataVigencia": datetime.today().strftime("%Y-%m-%d"),
        "fornecedor": "Fornecedor X",
        "telefonesFornecedor": [],
        "emailsFornecedor": [],
        "items": [],
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }

    ata_id = database.insert_ata(ata_data)
    atas = database.get_all_atas()
    assert any(a["id"] == ata_id for a in atas)
