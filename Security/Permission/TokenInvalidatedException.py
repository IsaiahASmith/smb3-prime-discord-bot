class TokenInvalidatedException(Exception):
    """The token is no longer in use"""
    def __init__(self, hole, message):
        self.hole = hole
        super.__init__(message)