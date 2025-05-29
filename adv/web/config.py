"""
Файл конфигураций Advertisement
"""
class BaseConfig:
    API_TITLE = 'Advertisement API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.0'
    OPENAPI_JSON_PATH = 'openapi/adv.json'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_REDOC_PATH = '/redoc'
    OPENAPI_REDOC_URL = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'  # noqa: E501
    OPENAPI_SWAGGER_UI_PATH = '/docs/adv'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'


class Production(BaseConfig):
    debug = False


class Development(BaseConfig):
    debug = True