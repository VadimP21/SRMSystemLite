"""
Файл подключения
"""

import logging

import tornado

from lead.web.routers import routers


def app():
    return tornado.web.Application(routers)


if __name__ == "__main__":
    try:
        app = app()
        app.listen(8000)
        logging.info("Server started on port 8000")  # Добавьте логирование
        tornado.ioloop.IOLoop.current().start()
    except OSError as e:
        logging.error(
            f"Failed to start server: {e}"
        )  # Обработка ошибки, например, занятый порт
    except Exception as e:
        logging.exception(
            f"An unexpected error occurred: {e}"
        )  # Логирование других исключений
