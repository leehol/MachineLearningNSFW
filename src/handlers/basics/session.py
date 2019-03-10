import logging

import functools
from common import response_utils


log = logging.getLogger(__name__)


class Session(object):
    def __init__(self):
        pass

    @staticmethod
    def determine_expires_days(user_level):
        """
        user level
            -2 banned user
            -1 anomous user
            0 normal user
            1 verified user
            2 editor
            3 admin
            100 super admin
        """

        if user_level == 100:
            return 30
        if user_level == 2:
            return 30
        if user_level == 1:
            return 180
        if user_level == 0:
            return 180
        if user_level == -1:
            return 180
        return 180

    # Override normal authenticated decorator
    @staticmethod
    def authenticated(http_method):
        """
        Decorate methods with this to require that the user be logged in.
        If the user is not authenticated by self.authenticate(), will return errCode=1005
        """

        @functools.wraps(http_method)
        def wrapper(self, *args, **kwargs):
            if not self.authenticate():
                self.write(response_utils.make_error_response(err_code=1005,
                                                              err_msg="Session expired. Please log in again."))
            else:
                return http_method(self, *args, **kwargs)

        return wrapper








