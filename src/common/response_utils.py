def make_success_response(data={}):
    return {
        "status": True,
        "data": data
    }


def make_error_response(err_msg="", err_code=-1, err_details={}):
    """
    -1 means you cannot show to users
    -2 means you can show to users
    :param err_msg:
    :param err_code:
    :param err_details:
    :return:
    """
    return {
        "status": False,
        "error": {
            "errCode": err_code,
            "errMsg": err_msg,
            "errDetails": err_details
        }
    }


def exception(func):
    """
    add decorator for functions
    :return: False
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return False
    return wrapper


def sanitize_input(data):
    for k, v in data.items():
        pass
