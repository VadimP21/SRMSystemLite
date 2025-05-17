from fastapi import FastAPI


app = FastAPI(
    debug=True,
)

from product.web.api import api
