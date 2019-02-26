#!/usr/bin/python3

from tornado.web import url

from .BaseRequestHandler import BaseRequestHandler
from .Main import Main

routes = [
    url(r'/', Main)
]