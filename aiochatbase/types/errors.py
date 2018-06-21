class ChatbaseException(Exception):
    def __init__(self, message=None):
        super(ChatbaseException, self).__init__(message)


class InvalidMessageTypeError(ChatbaseException):
    """
    Error raised when attribute values are set on a Message instance which is not compatible with
    the msg_type attribute.
    """
    pass


class ReceivedNoMessage(ChatbaseException):
    pass


class InvalidApiKey(ChatbaseException):
    def __init__(self):
        super().__init__('Your API key is invalid.')
