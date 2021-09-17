class DuplicateRowError(Exception):
    """duplicate row"""

    def __init__(self, data):
        super(DuplicateRowError, self).__init__()
        self.data = data


class NotFoundException(Exception):

    def __init__(self, message):
        self.message = message
