# -*- coding: utf-8 -*-
# filename: main.py
import web
from web.httpserver import runsimple
from handle import Handle

urls = (
    '/wx', 'Handle',
)


if __name__ == '__main__':
    app = web.application(urls, globals())
    runsimple(func=app.wsgifunc(), server_address=('0.0.0.0', 80))
