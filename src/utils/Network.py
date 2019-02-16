from http.client import responses

class NetworkResponse(object):

    def __init__(self, status_code: int, reason=None):
        assert status_code is not None, "Empty status code!"

        self.status_code = status_code
        self.reason = reason
        
        if reason is None:
            self.reason = responses[self.status_code]


class Panic(NetworkResponse):

    pass


class Success(NetworkResponse):

    pass