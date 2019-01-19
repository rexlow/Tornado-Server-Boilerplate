#!/usr/bin/python3

from loguru import logger
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from .BaseRequestHandler import BaseRequestHandler

from utils import formatRequestBody, unloadRequestParams
from configs import default_get_response

class Main(BaseRequestHandler):

    @coroutine
    def get(self):
        logger.info("[/] GET Request from: {}".format(self.request.remote_ip))
        result = yield self.handleGet()
        self.write(result)
        self.finish()

    @coroutine
    def post(self):
        logger.info("[/] POST Request from: {}".format(self.request.remote_ip))
        result = yield self.handlePost()
        self.write(result)
        self.finish()

    @run_on_executor
    def handleGet(self):
        if not self.request.arguments:
            return default_get_response

        data = unloadRequestParams(self.request.arguments)
        
        # do something with the data
        result = data
        return result

    @run_on_executor
    def handlePost(self):
        reqBody = self.request.body.decode('utf8').split("&")
        reqBody = formatRequestBody(reqBody)

        # do something
        return reqBody