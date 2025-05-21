from pathlib import Path

import yaml
from fastapi import FastAPI


app = FastAPI(
    debug=True, openapi_url="/openapi/products.json", docs_url="/docs/product"
)


oas_doc = yaml.safe_load((Path(__file__).parent / "../openapi.yaml").read_text())

app.openapi = lambda: oas_doc
from product.web.api import api
