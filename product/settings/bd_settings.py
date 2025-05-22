from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    @field_validator("DATABASE_URL")
    def validate_db_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v

    class Config:
        env_file = Path(__file__).parent / "../.env"
        extra = "allow"


settings = Settings()
