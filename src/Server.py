#!/usr/bin/python3

import time
import json
from loguru import logger
from tornado.ioloop import IOLoop
from tornado.web import Application, url
from tornado.httpserver import HTTPServer

from configs import server_configs
from routes import Main

class Server(Application):

    def __init__(self, **kwargs):
        kwargs["handlers"] = [
            url(r'/', Main)
        ]
        kwargs["debug"] = server_configs["debug"]
        super(Server, self).__init__(**kwargs)
        

if __name__ == "__main__":
    logger.info("Tornado Server running at {}:{}".format(server_configs["host"], server_configs["port"]))
    app = Server()
    server = HTTPServer(app)
    server.listen(port=server_configs["port"])
    IOLoop.instance().start()