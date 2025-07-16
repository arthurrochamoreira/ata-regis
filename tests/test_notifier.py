import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from datetime import datetime, timedelta
import database
from notifier import check_vigencias


def test_notification_trigger(monkeypatch, tmp_path):
    db_path = tmp_path / "notify.db"
    monkeypatch.setattr(database, "DATABASE_NAME", str(db_path))
    database.create_tables()

    ata_data = {
        "numeroAta": "0002/2024",
        "documentoSei": "21482503",
        "objeto": "Teste",
        "dataAssinatura": "2024-01-01",
        "dataVigencia": (datetime.today() + timedelta(days=80)).strftime("%Y-%m-%d"),
        "fornecedor": "Fornecedor",
        "telefonesFornecedor": [],
        "emailsFornecedor": [],
        "items": [],
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    database.insert_ata(ata_data)

    sent = {}

    def fake_send_email(sub, body):
        sent['ok'] = True

    monkeypatch.setattr('notifier.send_email', fake_send_email)

    check_vigencias()

    assert sent.get('ok')
