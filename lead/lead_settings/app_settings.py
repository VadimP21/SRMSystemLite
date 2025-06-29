import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Settings:
    """Настройки приложения."""

    base_dir: str = field(
        default_factory=lambda: os.path.dirname(os.path.abspath(__file__))
    )
    database_url: str = field(
        default_factory=lambda: os.environ.get(
            "DATABASE_URL", "sqlite:///./database.db"
        )
    )
    sqlalchemy_database_uri: str = field(init=False)
    sqlalchemy_track_modifications: bool = False
    port: int = field(default_factory=lambda: int(os.environ.get("PORT", 8000)))
    debug: bool = field(
        default_factory=lambda: os.environ.get("DEBUG", "False").lower() == "true"
    )
    secret_key: str = field(default_factory=lambda: os.environ.get("SECRET_KEY"))

    log_level: str = "INFO"
    log_file: Optional[str] = None

    redis_host: Optional[str] = None
    redis_port: Optional[int] = None
    redis_password: Optional[str] = None
    redis_db: Optional[int] = None

    def __post_init__(self):
        self.sqlalchemy_database_uri = self.database_url


def get_settings():
    return Settings()
