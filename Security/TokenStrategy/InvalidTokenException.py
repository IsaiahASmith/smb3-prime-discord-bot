class InvalidTokenException(Exception):
    """
    An error to be raised when there is an invalid token is attempted to be created.
    This is a generic exception, instead a subclass should be raised in most cases.
    """