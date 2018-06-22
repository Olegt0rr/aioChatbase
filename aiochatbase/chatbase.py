import logging
from datetime import datetime

from .types import Message, MessageTypes, Click, Event

logger = logging.getLogger(f'chatbase')


class Chatbase:
    def __init__(self, api_key, platform):
        """
        :param api_key: Chatbase API token key
        :type api_key: str

        :param platform: your chat bot platform (Telegram, Facebook, Android, etc.)
        :type platform: str
        """
        self.api_key = api_key
        self.platform = platform

    async def register_message(self, user_id, intent=None, message=None, not_handled=None, version=None,
                               session_id=None, message_type=MessageTypes.USER,
                               time_stamp=datetime.now().timestamp()):
        """
        Register message

        :param user_id: chatbot user id
        :type user_id: str

        :param intent: chatbot user intention
        :type intent: str

        :param message: user full message
        :type message: str

        :param not_handled: True if your bot don't understand user intention
        :type not_handled: bool

        :param version: fill to track versions of your code
        :type version: str

        :param session_id: fill to track your own custom sessions
        :type session_id: str

        :param message_type: "user" or "agent" (aka your chatbot)
        :type message_type: str

        :param time_stamp: milliseconds since the UNIX epoch, used to sequence messages.
        :type time_stamp: int

        :return: Chatbase message id
        :rtype: str
        """
        message = Message(api_key=self.api_key,
                          message_type=message_type,
                          user_id=user_id,
                          time_stamp=int(time_stamp * 1000),
                          platform=self.platform,
                          message=message,
                          intent=intent,
                          not_handled=not_handled,
                          version=version,
                          session_id=session_id)
        cb_msg_id = await message.send()
        logger.debug(f"Registered {self.platform} message from {message_type} {user_id} with intent '{intent}'. "
                     f"Message id: {cb_msg_id}. ")
        return cb_msg_id

    async def register_click(self, url, user_id=None, version=None):
        """
        Register clicked URL

        :param url: clicked URL
        :type url: str

        :param user_id: chatbot user id
        :type user_id: str

        :param version: fill to track versions of your code
        :type version: str

        :return: True if result is OK
        :rtype bool
        """
        click = Click(self.api_key, url, self.platform, user_id=user_id, version=version)
        result = await click.send()
        logger.debug(f"Registered {self.platform} click from user {user_id} to url '{url}'. ")
        return result

    async def register_event(self, user_id, intent, time_stamp=datetime.now().timestamp(),
                             version=None, properties=None):
        """
        Register event

        :param user_id: chatbot user id
        :type user_id: str

        :param intent: chatbot user intention
        :type intent: str

        :param time_stamp: milliseconds since the UNIX epoch, used to sequence messages.
        :type time_stamp: int

        :param version: fill to track versions of your code
        :type version: str

        :param properties: misc properties
        :type properties: dict

        :return: True if result is OK
        :rtype: bool
        """
        event = Event(api_key=self.api_key,
                      user_id=user_id,
                      intent=intent,
                      timestamp_millis=int(time_stamp * 1000),
                      platform=self.platform,
                      version=version,
                      properties=properties)
        result = await event.send()
        logger.debug(f"Registered {self.platform} event from user {user_id} with intent {intent}. ")
        return result
