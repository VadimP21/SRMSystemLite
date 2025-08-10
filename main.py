import logging

import tornado
from fastapi import FastAPI

from adv.web.app import create_app
from lead.app import app
from lead.lead_settings.app_settings import Settings
from product.settings.app_settings import settings

if __name__ == "__main__":
    adv_app = create_app()
    adv_app.run(debug=adv_app.config["DEBUG"])

    product_app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=True,
        openapi_url="/openapi/products.json",
        docs_url="/docs/product",
    )

    try:
        lead_app = app()
        lead_app.listen(Settings.port)
        logging.info("Server started on port 8000")
        tornado.ioloop.IOLoop.current().start()
    except OSError as e:
        logging.error(f"Failed to start server: {e}")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
