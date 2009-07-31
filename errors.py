import socket

class ForOFourException(Exception):
    pass

class HTTPError(ForOFourException):
    def __init__(self, originalException):
        self.originalException = originalException
    def __str__(self):
        return str(self.originalException.code)

class URLError(ForOFourException):
    def __init__(self, originalException):
        self.originalException = originalException
    def __str__(self):
        # FIXME: not sure this is good enough behaviour that covers all possible reasons
        if isinstance(self.originalException.reason, socket.timeout):
            return 'TIMEOUT'
        else:
            return error.reason.args[1]

class HTMLError(ForOFourException):
    def __init__(self, originalException):
        self.originalException = originalException
    def __str__(self):
        message = str(self.originalException)
        if len(message) > 40:
            message = message[0:40] + '... (truncated)'
        return 'PARSER: ' + message
