class APrawcoreException(Exception):
    """Base exception class for exceptions that occur within this package."""


class InvalidInvocation(APrawcoreException):
    """Indicate that the code to execute cannot be completed."""


class RequestException(APrawcoreException):
    # yoinked this from praw
    def __init__(self, original_exception, request_args, request_kwargs):
        self.original_exception = original_exception
        self.request_args = request_args
        self.request_kwargs = request_kwargs
        super(RequestException, self).__init__('error with request {}'
                                               .format(original_exception))
