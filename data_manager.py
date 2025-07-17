from __future__ import annotations

import copy
import datetime
from typing import Any, Dict, List

import database


class DataManager:
    """Camada de acesso a dados utilizada pela aplicacao."""

    def __init__(self, db: database.Database | None = None) -> None:
        # Permite injecao de dependencia para facilitar testes
        self.db = db or database._DB
        self.db.init_db()

    # ------------------------------------------------------------------
    def get_all_records(self) -> List[Dict[str, Any]]:
        return self.db.get_all_atas()

    # ------------------------------------------------------------------
    def get_record(self, record_id: int) -> Dict[str, Any] | None:
        for record in self.db.get_all_atas():
            if record["id"] == record_id:
                return record
        return None

    # ------------------------------------------------------------------
    def add_record(self, data: Dict[str, Any]) -> None:
        timestamp = datetime.datetime.now().isoformat()
        payload = copy.deepcopy(data)
        payload["createdAt"] = timestamp
        payload["updatedAt"] = timestamp
        self.db.insert_ata(payload)

    # ------------------------------------------------------------------
    def update_record(self, record_id: int, data: Dict[str, Any]) -> None:
        payload = copy.deepcopy(data)
        payload["updatedAt"] = datetime.datetime.now().isoformat()
        self.db.update_ata(record_id, payload)

    # ------------------------------------------------------------------
    def delete_record(self, record_id: int) -> None:
        self.db.delete_ata(record_id)
