from abc import abstractmethod
import tornado.web
from tornado import gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import json
import socket
import logging


# user defined packages
from ..handler_utils import parse_input
from ..handler_utils import parse_urlencoded
from .session import Session


MAX_WORKERS = 20

log = logging.getLogger(__name__)


class BasicHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    """
    basic type for all other handlers
    """
    def set_default_headers(self):
        origin = self.request.headers.get('Origin', "")
        self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header("Accept-Encoding", "gzip")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Accept")

    def initialize(self):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("user_hash")

    def set_current_user(self, user_hash, expires_days):
        self.set_secure_cookie(name="user_hash", value=user_hash, expires_days=expires_days)

    def authenticate(self):
        return True

    def options(self):
        return

    def verify(self, require_ip=False):
        data = getattr(self.request, 'request_data', None)
        if require_ip:
            ip = self.parse_client_ip()
            if ip is not None:
                data["ip"] = ip
                data["register_ip"] = ip
        return data

    @Session.authenticated
    @tornado.gen.coroutine
    def post(self):
        res = yield self.determine_status()
        self.write(res)

    @Session.authenticated
    @tornado.gen.coroutine
    def get(self):
        res = yield self.determine_status()
        self.write(res)

    @abstractmethod
    @run_on_executor
    def background_task(self):
        pass

    def determine_status(self):
        resp = self.background_task()
        return resp

    def prepare(self):
        """
        This is before passing the security check , and before any http method: get/post/option
        Should be override if you don't want to process data, otherwise will parse the request data for each request
        :return:
        """
        # Don't do any process and auth for option call
        if self.request.method == "OPTIONS":
            return

        if getattr(self.request, 'request_data', None):
            return
        try:
            setattr(self.request, 'request_data', self.process_data())
        except Exception as e:
            log.error("Error preparing request data", exc_info=True)
        return

    def process_data(self):
        try:
            log.info("Received User %s request for %s", self.request.method, self.__class__.__name__)
            content_type = self.request.headers.get("Content-Type", "")
            if content_type.startswith("application/json"):
                data = json.loads(self.request.body, encoding="utf8")
                self.set_header("Content-Type", "application/json")
            elif content_type.startswith("application/x-www-form-urlencoded"):
                data = parse_urlencoded(self.request.body)
            elif content_type.startswith("multipart/form-data"):
                data = self.process_multipart_data()
            else:
                data = parse_input(self.request.uri)

        except Exception as e:
            log.error("Error parsing request data", exc_info=True)
            return {}
        return data

    def process_multipart_data(self):
        data = {}

        for key, value in self.request.files.items():
            if "binary" in key:
                data[key] = value[0]["body"]
            elif isinstance(value[0]["body"], bytes):
                data[key] = value[0]["body"].decode("utf8")
            else:
                data[key] = value[0]["body"]

        for key, value in self.request.body_arguments.items():
            data[key] = value[0].decode("utf8")
        return data

    def validate_ip(self, addr):
        try:
            socket.inet_pton(socket.AF_INET, addr)
            return True
        except socket.error:
            log.warning("Invalid IP address")
            return False

    def parse_client_ip(self):
        try:
            ips = self.request.headers.get_list("X-Forwarded-For")
            if len(ips) == 0:
                log.error("USER_AUTHENTICATE EXCEPTION could not find ip from headers.")
                return "No ips in headers."
            ips = ips[0]
            ips = ips.strip("\r\n")
            ips = ips.split(',')
            return ips[0]
        except Exception as e:
            log.error("USER_AUTHENTICATE EXCEPTION parse_client_ip e=%s" % str(e))
            return "Unknown IP"
