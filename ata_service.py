from __future__ import annotations

from typing import Any, Dict, List

from data_manager import DataManager


class AtaService:
    """Camada de negócio usada pela aplicação."""

    def __init__(self, data_manager: DataManager | None = None) -> None:
        self.data_manager = data_manager or DataManager()

    # -------------------------------
    def list_atas(self) -> List[Dict[str, Any]]:
        return self.data_manager.get_all_records()

    def get_ata(self, ata_id: int) -> Dict[str, Any] | None:
        return self.data_manager.get_record(ata_id)

    def add_ata(self, ata_data: Dict[str, Any]) -> None:
        self.data_manager.add_record(ata_data)

    def update_ata(self, ata_id: int, ata_data: Dict[str, Any]) -> None:
        self.data_manager.update_record(ata_id, ata_data)

    def delete_ata(self, ata_id: int) -> None:
        self.data_manager.delete_record(ata_id)
