import logging

# user defined packages
from .base_handler import BasicHandler

log = logging.getLogger(__name__)


class SecuredHandler(BasicHandler):
    def set_default_headers(self):
        super().set_default_headers()
        self.set_header("Access-Control-Allow-Headers", "x-xsrftoken, content-type, Accept")
        self.set_header("Access-Control-Allow-Credentials", "true")

    def authenticate(self):
        data = getattr(self.request, 'request_data', None)
        if not isinstance(data, dict):
            log.error("USER_AUTHENTICATE authenticate invalid data. data=%s" % data)
            return False

        ignore_security_check = data.get("ignore_security_check")
        if ignore_security_check is not None:
            return True

        if not self.current_user:
            log.error("USER_AUTHENTICATE authenticate invalid cookie. data=%s" % data)
            return False

        return True

    def process_data(self):
        data = super().process_data()
        if self.current_user and str(self.current_user, 'utf-8', 'ignore'):
            data["cookie_user_hash"] = str(self.current_user, 'utf-8', 'ignore')
        return data
