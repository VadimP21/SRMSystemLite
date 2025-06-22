"""
Маршрутизаторы проекта
"""

from tornado.web import URLSpec

from lead.web.api import Lead, Leads

routers = [
    URLSpec(r"/leads/?(\d+)?", Lead),
    URLSpec(r"/leads/list/", Leads),
]
