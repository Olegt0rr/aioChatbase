import logging
from typing import List

from .basic import BasicChatbaseObject
from ..utils import json
from ..types.errors import ChatbaseException, InvalidUserIdType

logger = logging.getLogger(f'chatbase.{__name__}')


class Message(BasicChatbaseObject):
    def __init__(self, api_key, message_type, user_id, time_stamp, platform, message=None, intent=None,
                 not_handled=None, version=None, session_id=None, session=None):
        """

        :param api_key: the Chatbase ID of the bot
        :type api_key: str

        :param message_type: valid values "user" or "agent" (aka your bot) message.
                            Field was renamed from API "type", cause "type" name already used in Python's namespace.
        :type message_type: str

        :param user_id: the ID of the end-user
        :type user_id: str or int

        :param time_stamp: milliseconds since the UNIX epoch, used to sequence messages.
                            (must be within previous 30 days)
        :type time_stamp: int

        :param platform: valid values "Facebook", "SMS", "Web", "Android", "iOS", "Actions", "Alexa", "Cortana", "Kik",
                            "Skype", "Twitter", "Viber", "Telegram", "Slack", "WhatsApp", "WeChat", "Line", "Kakao"
                            or a custom name like "Workplace" or "OurPlatform"
        :type platform: str

        :param message: the raw message body regardless of type for example a typed-in or a tapped button or
                        tapped image; 1,200 characters max
        :type message:

        :param intent: set for user messages only; if not set usage metrics will not be shown per intent; do not set
                        if it is a generic catch all intent, like default fallback, so that clusters of similar
                        messages can be reported
        :type intent: str

        :param not_handled: set for user messages only; indicates that the bot was not able to handle the message
                            because it was not understood (e.g. no intent for "Start over"), or it was understood
                            (e.g. has intent for "Order drink") but not supported; if not set then these high churn
                            issues are not shown across reports; set for generic catch all intents, like default
                            fallback
        :type not_handled: bool

        :param version: set for user and bot messages; used to track versions of your code or to track A/B tests
        :type version: str

        :param session_id: set for user and bot messages; used to define your own custom sessions for Session Flow
                            report and daily session metrics
        :type session_id: str
        """
        # check input
        if not (isinstance(user_id, str) or isinstance(user_id, int)):
            raise InvalidUserIdType()

        # aiohttp
        self.session = session

        # required
        self.api_key = api_key
        self.user_id = str(user_id)
        self.message_type = message_type
        self.time_stamp = time_stamp
        self.platform = platform

        # optional
        self.message = message
        self.intent = intent
        self.not_handled = not_handled
        self.version = str(version)
        self.session_id = str(session_id)

        # settings
        self._api_url = f"https://chatbase.com/api/message"

    def to_dict(self):
        """ Return a dict version for use with the Chatbase API """

        data = {
            'api_key': self.api_key,
            'type': self.message_type,
            'user_id': self.user_id,
            'time_stamp': self.time_stamp,
            'platform': self.platform,
        }

        if self.message:
            data['message'] = self.message

        if self.intent:
            data['intent'] = self.intent

        if self.not_handled:
            data['not_handled'] = self.not_handled

        if self.version:
            data['version'] = self.version

        if self.session_id:
            data['session_id'] = self.session_id

        return data

    def to_json(self):
        """ Return a JSON version for use with the Chatbase API """
        data = self.to_dict()
        return json.dumps(data)

    async def check(self):
        from ..types import MessageTypes, InvalidMessageTypeError

        # message_type only user and agent
        if self.message_type not in (MessageTypes.USER, MessageTypes.AGENT):
            raise InvalidMessageTypeError('message_type: valid values "user" or "agent".')

        # Only user-type Messages can have the not_handled attribute as True.
        if self.not_handled and self.message_type == MessageTypes.AGENT:
            raise InvalidMessageTypeError('Cannot set not_handled as True when msg is of type Agent.')

        # Only user-type Messages can be with defined intentions.
        if self.intent and self.message_type == MessageTypes.AGENT:
            raise InvalidMessageTypeError('Cannot set intent for agent messages.')

        # Message length limit - 1200 characters
        if self.message and len(self.message) > 1200:
            self.message = self.message[:1200]

        return True

    async def send(self):
        await self.check()
        result = await self._send(session=self.session)
        return result.get('message_id')


class Messages(BasicChatbaseObject):
    def __init__(self, message_list, session=None):
        """
        :param message_list:
        :type message_list: List[Message]
        """
        # aiohttp
        self.session = session

        self.messages = message_list
        self._api_url = 'https://chatbase.com/api/messages'

    def to_json(self):
        """ Return a JSON version for use with the Chatbase API """

        data = {
            'messages': [m.to_dict() for m in self.messages]
        }
        return json.dumps(data)

    async def send(self):
        for m in self.messages:
            await m.check()

        result = await self._send(session=self.session)
        responses = result.get('responses')

        if not result.get('all_succeeded'):
            for r in responses:
                if r.get('status') == 400:
                    raise ChatbaseException(r.get('reason'))

        return [r.get('message_id') for r in responses]
