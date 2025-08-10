"""
Файл подключения
"""

import logging

import tornado

from lead.lead_settings.app_settings import Settings
from lead.web.routers import routers


def app():
    return tornado.web.Application(routers)


if __name__ == "__main__":
    try:
        app = app()
        app.listen(Settings.port)
        logging.info("Server started on port 8000")
        tornado.ioloop.IOLoop.current().start()
    except OSError as e:
        logging.error(f"Failed to start server: {e}")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
