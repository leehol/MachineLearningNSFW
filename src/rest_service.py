import os
from tornado.httpserver import HTTPServer
import tornado.web
import logging
import tornado.ioloop
import gb


log = logging.getLogger(__name__)

from tornado_route import routes


def get_tornado_application():
    return tornado.web.Application(routes)


tornado_app = get_tornado_application()


def start_tornado_server():
    server = HTTPServer(tornado_app, xheaders=True)
    server.bind(gb.app_port)
    # start multiple tornado process
    server.start()
    log.info("Tornado Server is up!!! on PORT %s", gb.app_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_tornado_server()
