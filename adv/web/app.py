"""
Инициализация объекта приложения Flask и объекта Api
"""
from flask import Flask
from flask_smorest import Api

from adv.web.api.api import blueprint
from adv.web.config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)

adv_api = Api(app)

adv_api.register_blueprint(blueprint)

