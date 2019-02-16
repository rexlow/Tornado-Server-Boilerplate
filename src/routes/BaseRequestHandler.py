import json
import traceback
from tornado import escape
from tornado.util import unicode_type
from tornado.web import RequestHandler, url, HTTPError
from concurrent.futures.thread import ThreadPoolExecutor
from configs import server_configs
from utils.Network import Success, Panic

class BaseRequestHandler(RequestHandler):

    executor = ThreadPoolExecutor(max_workers=server_configs["max_workers"])

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Expose-Headers", "*")
        self.set_header("Access-Control-Allow-Credentials", "false")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header('Content-Type', 'application/json')

    def response(self, responseObject):

        if isinstance(responseObject, Success):
            self.write(responseObject)

        if isinstance(responseObject, Panic):
            self.write_error(responseObject)

        if isinstance(responseObject, str):
            self.set_header('Content-Type', 'text/html; charset=UTF-8')
            self.write(responseObject)

    def write(self, chunk):

        if self._finished:
            raise RuntimeError("Cannot write() after finish()")

        if not isinstance(chunk, (bytes, unicode_type, dict, Success)):
            message = "write() only accepts bytes, unicode, dict, Success objects"
            if isinstance(chunk, list):
                message += ". Lists not accepted for security reasons; see " + \
                    "http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.write"
            raise TypeError(message)

        if isinstance(chunk, dict):
            logger.error("its dict")
            chunk = escape.json_encode(chunk)
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        if isinstance(chunk, Success):
            chunk = escape.json_encode(chunk.reason)
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        chunk = escape.utf8(chunk)
        self._write_buffer.append(chunk)
        self.finish()

    def write_error(self, error, **kwargs):

        self.set_status(error.status_code)
        self.set_header('Content-Type', 'application/json')
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = [l for l in traceback.format_exception(*kwargs["exc_info"])]
            
            self.finish(json.dumps({
                'error': {
                    'message': error.reason,
                    'traceback': lines,
                }
            }))
        else:
            self.finish(json.dumps({
                'error': {
                    'message': error.reason,
                }
            }))