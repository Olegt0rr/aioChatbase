import asyncio
import logging
from datetime import datetime

from .types import Message, Messages, MessageTypes, Click, Event

logger = logging.getLogger(f'chatbase')


class Chatbase:
    def __init__(self, api_key, platform, task_mode=False):
        """
        :param api_key: Chatbase API token key
        :type api_key: str

        :param platform: your chat bot platform (Telegram, Facebook, Android, etc.)
        :type platform: str

        :param task_mode: returns asyncio.Task in register_* methods
        :type task_mode: bool
        """

        self.api_key = api_key
        self.platform = platform
        self.task_mode = task_mode

    async def prepare_message(self, user_id, intent=None, message=None, not_handled=None, version=None,
                              session_id=None, message_type=MessageTypes.USER,
                              time_stamp=datetime.now().timestamp()):
        """
        Prepare message

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

        :param time_stamp: seconds since the UNIX epoch, used to sequence messages.
        :type time_stamp: float

        :return: Chatbase message
        :rtype: Message
        """
        return Message(api_key=self.api_key,
                       message_type=message_type,
                       user_id=user_id,
                       time_stamp=int(time_stamp * 1000),
                       platform=self.platform,
                       message=message,
                       intent=intent,
                       not_handled=not_handled,
                       version=version,
                       session_id=session_id)

    async def register_message(self, user_id, intent=None, message=None, not_handled=None, version=None,
                               session_id=None, message_type=MessageTypes.USER,
                               time_stamp=datetime.now().timestamp(), task=None):
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

         :param time_stamp: seconds since the UNIX epoch, used to sequence messages.
         :type time_stamp: int

         :param task: Returns aio.Task if True, returns result if False, default value if None
         :type task: bool

         :return: Chatbase message id
         :rtype: str
         """

        coroutine = self._register_message(user_id=user_id, intent=intent, message=message, not_handled=not_handled,
                                           version=version, session_id=session_id, message_type=message_type,
                                           time_stamp=time_stamp)
        if isinstance(task, bool):
            if not task:
                return await coroutine
            return asyncio.ensure_future(coroutine)

        if self.task_mode:
            return asyncio.ensure_future(coroutine)

        return await coroutine

    async def _register_message(self, user_id, intent=None, message=None, not_handled=None, version=None,
                                session_id=None, message_type=MessageTypes.USER,
                                time_stamp=datetime.now().timestamp()):
        message = await self.prepare_message(user_id, intent=intent, message=message, not_handled=not_handled,
                                             version=version, session_id=session_id, message_type=message_type,
                                             time_stamp=time_stamp)
        cb_msg_id = await message.send()
        logger.debug(f"Registered {self.platform} message from {message_type} {user_id} with intent '{intent}'. "
                     f"Message id: {cb_msg_id}. ")
        return cb_msg_id

    async def register_messages(self, message_list):
        """
        :param message_list:
        :type message_list: List[Message]

        :return: list of Chatbase message ids
        :rtype: List[str]
        """
        messages = Messages(message_list)
        msgs_id_list = await messages.send()
        logger.debug(f"Registered {self.platform} messages: {msgs_id_list}")
        return msgs_id_list

    async def register_click(self, url, user_id=None, version=None, task=None):
        """
        Register clicked URL

        :param url: clicked URL
        :type url: str

        :param user_id: chatbot user id
        :type user_id: str

        :param version: fill to track versions of your code
        :type version: str

        :param task: Returns aio.Task if True, returns result if False, default value if None
        :type task: bool

        :return: True if result is OK
        :rtype bool
        """

        coroutine = self._register_click(url=url, user_id=user_id, version=version)

        if isinstance(task, bool):
            if not task:
                return await coroutine
            return asyncio.ensure_future(coroutine)

        if self.task_mode:
            return asyncio.ensure_future(coroutine)

        return await coroutine

    async def _register_click(self, url, user_id=None, version=None):
        click = Click(self.api_key, url, self.platform, user_id=user_id, version=version)
        result = await click.send()
        logger.debug(f"Registered {self.platform} click from user {user_id} to url '{url}'. ")
        return result

    async def register_event(self, user_id, intent, time_stamp=datetime.now().timestamp(), version=None,
                             properties=None, task=None):
        """
        Register event

        :param user_id: chatbot user id
        :type user_id: str

        :param intent: chatbot user intention
        :type intent: str

        :param time_stamp: seconds since the UNIX epoch, used to sequence messages.
        :type time_stamp: float

        :param version: fill to track versions of your code
        :type version: str

        :param properties: misc properties
        :type properties: dict

        :param task: Returns aio.Task if True, returns result if False, default value if None
        :type task: bool

        :return: True if result is OK
        :rtype: bool
        """
        coroutine = self._register_event(user_id=user_id, intent=intent, time_stamp=time_stamp, version=version,
                                         properties=properties)

        if isinstance(task, bool):
            if not task:
                return await coroutine
            return asyncio.ensure_future(coroutine)

        if self.task_mode:
            return asyncio.ensure_future(coroutine)

        return await coroutine

    async def _register_event(self, user_id, intent, time_stamp=datetime.now().timestamp(),
                              version=None, properties=None):
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
