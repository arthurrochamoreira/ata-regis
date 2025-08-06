from dataclasses import dataclass, field
from os import getenv
from typing import List, Dict


@dataclass
class Settings:
    """Application configuration loaded from environment variables."""

    DB_FILE: str = getenv("DB_FILE", "atas.db")
    DEFAULT_EMAIL_RECIPIENTS: List[str] = field(
        default_factory=lambda: getenv(
            "DEFAULT_EMAIL_RECIPIENTS",
            "diatu@trf1.jus.br,seae1@trf1.jus.br",
        ).split(",")
    )
    ALERT_THRESHOLDS: Dict[int, str] = field(
        default_factory=lambda: {
            90: "D-90",
            60: "D-60",
            30: "D-30",
            15: "D-15",
            7: "D-7",
            1: "D-1",
            0: "VENCIMENTO",
        }
    )
    POST_EXPIRY_DAYS: int = int(getenv("POST_EXPIRY_DAYS", "30"))
    VENCIMENTO_ALERT_DAYS: int = int(getenv("VENCIMENTO_ALERT_DAYS", "90"))
    JSON_DATA_FILE: str = getenv("JSON_DATA_FILE", "atas.json")
    SCHEDULER_INTERVAL: int = int(getenv("SCHEDULER_INTERVAL", "300"))
    DAILY_CHECK_HOUR: int = int(getenv("DAILY_CHECK_HOUR", "9"))
    DAILY_CHECK_MINUTE: int = int(getenv("DAILY_CHECK_MINUTE", "0"))
    WEEKLY_CHECK_WEEKDAY: int = int(getenv("WEEKLY_CHECK_WEEKDAY", "0"))
    WEEKLY_CHECK_HOUR: int = int(getenv("WEEKLY_CHECK_HOUR", "8"))
    WEEKLY_CHECK_MINUTE: int = int(getenv("WEEKLY_CHECK_MINUTE", "0"))
    MONTHLY_CHECK_DAY: int = int(getenv("MONTHLY_CHECK_DAY", "1"))
    MONTHLY_CHECK_HOUR: int = int(getenv("MONTHLY_CHECK_HOUR", "7"))
    MONTHLY_CHECK_MINUTE: int = int(getenv("MONTHLY_CHECK_MINUTE", "0"))
    FONT_URL: str = getenv(
        "FONT_URL",
        "https://fonts.gstatic.com/s/inter/v7/Inter-Regular.ttf",
    )
    PAGE_TITLE: str = getenv(
        "PAGE_TITLE", "Ata de Registro de Preços 0016/2024"
    )


settings = Settings()
