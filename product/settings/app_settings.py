from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    SECRET_KEY: str
    DEBUG: bool

    class Config:
        env_file = Path(__file__).parent / "../.env"
        extra = "allow"


settings = Settings()
