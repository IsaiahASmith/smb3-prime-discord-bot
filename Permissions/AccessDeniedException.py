class AccessDeniedException(Exception):
    """The user does not have permission to access the hole"""
    def __init__(self, hole, message):
        self.hole = hole
        super.__init__(message)