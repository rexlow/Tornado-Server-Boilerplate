#!/usr/bin/python3

import simplejson
from loguru import logger
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from .BaseRequestHandler import BaseRequestHandler

from utils import unloadRequestParams, Success
from configs import default_get_response

class Main(BaseRequestHandler):

    @coroutine
    def get(self):
        logger.info("[/] GET Request from: {}".format(self.request.remote_ip))
        result = yield self.handleGet()
        self.response(result)

    @coroutine
    def post(self):
        logger.info("[/] POST Request from: {}".format(self.request.remote_ip))
        result = yield self.handlePost()
        self.response(result)

    @run_on_executor
    def handleGet(self):
        if not self.request.arguments:
            return default_get_response

        result = unloadRequestParams(self.request.arguments)

        # do something with the data
        return Success(200, result)

    @run_on_executor
    def handlePost(self):
        data = simplejson.loads(self.request.body)

        # do something with the data
        return Success(200, data)