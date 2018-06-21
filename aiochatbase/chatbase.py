from datetime import datetime

from .types import Message, MessageTypes, Click, Event


class Chatbase:
    def __init__(self, api_key, platform):
        """
        :param api_key:
        :type api_key: str
        :param platform:
        :type platform: str
        """
        self.api_key = api_key
        self.platform = platform

    async def register_message(self, user_id, intent=None, message=None, not_handled=None, version=None,
                               session_id=None, message_type=MessageTypes.USER,
                               time_stamp=datetime.now().timestamp()):
        """
        :type user_id: str
        :type intent: str
        :type message: str
        :type not_handled: bool
        :type version: str
        :type session_id: str
        :type message_type: str
        :type time_stamp: int

        :return: Chatbase message id
        :rtype: str
        """
        message = Message(api_key=self.api_key,
                          message_type=message_type,
                          user_id=user_id,
                          time_stamp=int(time_stamp),
                          platform=self.platform,
                          message=message,
                          intent=intent,
                          not_handled=not_handled,
                          version=version,
                          session_id=session_id)
        return await message.send()

    async def register_click(self, url, user_id=None, version=None):
        """

        :param url:
        :param user_id:
        :param version:
        :return: True if OK
        :rtype bool
        """
        click = Click(self.api_key, url, self.platform, user_id=user_id, version=version)
        return await click.send()

    async def register_event(self, user_id, intent, timestamp=datetime.now().timestamp(), platform=None, version=None,
                             properties=None):
        event = Event(api_key=self.api_key,
                      user_id=user_id,
                      intent=intent,
                      timestamp_millis=int(timestamp * 1000),
                      platform=platform,
                      version=version,
                      properties=properties)
        return await event.send()
