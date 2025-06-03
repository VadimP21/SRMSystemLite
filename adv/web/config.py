"""
Файл конфигураций Advertisement
"""

import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_default_secret_key_for_dev")

    API_TITLE = "Advertisement API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.0"
    OPENAPI_JSON_PATH = "openapi/adv.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"  # noqa: E501
    OPENAPI_SWAGGER_UI_PATH = "/docs/adv"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///crm.db")

    SQLALCHEMY_POOL_SIZE = int(os.environ.get("SQLALCHEMY_POOL_SIZE", 5))
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get("SQLALCHEMY_MAX_OVERFLOW", 10))
    SQLALCHEMY_POOL_TIMEOUT = int(os.environ.get("SQLALCHEMY_POOL_TIMEOUT", 30))
    SQLALCHEMY_POOL_RECYCLE = int(os.environ.get("SQLALCHEMY_POOL_RECYCLE", 3600))


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL", "sqlite:///crm.db")
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "super_secret_dev_key"


class TestingConfig(BaseConfig):
    """Конфигурация для тестирования."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "test_secret_key"


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
