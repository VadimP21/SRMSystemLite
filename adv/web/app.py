"""
Инициализация объекта приложения Flask и объекта Api
"""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from sqlalchemy import create_engine

from adv.web.api.api import blueprint
from adv.web.config import config_by_name


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()
    app.config.from_object(config_by_name[config_name])

    try:
        app.config.from_pyfile("config_prod.py", silent=True)
    except FileNotFoundError:
        pass
    except Exception as e:
        app.logger.warning(f"Ошибка загрузки конфигурации из instance/: {e}")

    engine = create_engine(
        app.config["SQLALCHEMY_DATABASE_URL"],
    )

    app.db_engine = engine

    adv_api = Api(app)

    adv_api.register_blueprint(blueprint)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"])
