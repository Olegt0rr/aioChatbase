class ChatbaseException(Exception):
    def __init__(self, message=None):
        super(ChatbaseException, self).__init__(message)


class InvalidMessageTypeError(ChatbaseException):
    """
    Error raised when attribute values are set on a Message instance which is not compatible with
    the msg_type attribute.
    """
    pass


class NotHandledAgentMessage(ChatbaseException):
    """
    Error raised when attribute not handled is True with agent message.
    Agent messages can't be not handled

    """
    pass


class IntentInAgentMessage(ChatbaseException):
    """
    Error raised when attribute intent set for agent message

    """
    pass


class ReceivedNoMessage(ChatbaseException):
    pass


class InvalidApiKey(ChatbaseException):
    def __init__(self):
        super().__init__('Your API key is invalid.')


class InvalidUserIdType(ChatbaseException):
    def __init__(self):
        super().__init__('User id must be string or integer.')
