from pathlib import Path

import yaml
from fastapi import FastAPI

from product.settings.app_settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=True,
    openapi_url="/openapi/products.json",
    docs_url="/docs/product",
)


# oas_doc = yaml.safe_load((Path(__file__).payrent / "../openapi.yaml").read_text())
#
# app.openapi = lambda: oas_doc
from product.web.api import api
