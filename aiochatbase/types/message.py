import json
import logging

from .basic import BasicChatbaseObject

logger = logging.getLogger(f'chatbase.{__name__}')


class Message(BasicChatbaseObject):
    def __init__(self, api_key, message_type, user_id, time_stamp, platform, message=None, intent=None,
                 not_handled=None, version=None, session_id=None):
        """

        :param api_key: the Chatbase ID of the bot
        :type api_key: str

        :param message_type: valid values "user" or "agent" (aka your bot) message.
                            Field was renamed from API "type", cause "type" name already used in Python's namespace.
        :type message_type: str

        :param user_id: the ID of the end-user
        :type user_id: str

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
        # required
        self.api_key = api_key
        self.message_type = message_type
        self.user_id = user_id
        self.time_stamp = time_stamp
        self.platform = platform

        # optional
        self.message = message
        self.intent = intent
        self.not_handled = not_handled
        self.version = version
        self.session_id = session_id

        self._api_url = f"https://chatbase.com/api/message"

    def to_json(self):
        """ Return a JSON version for use with the Chatbase API """

        data = {
            'api_key': self.api_key,
            'type': self.message_type,
            'user_id': self.user_id,
            'time_stamp': self.time_stamp,
            'platform': self.platform,
            'message': self.message or '',
            'intent': self.intent or '',
            'not_handled': self.not_handled or False,
            'version': self.version or '',
            'session_id': self.session_id or ''
        }
        return json.dumps(data)

    async def check(self):
        from ..types import MessageTypes, InvalidMessageTypeError

        # Only user-type Messages can have the not_handled attribute as True.
        if self.not_handled and self.message_type == MessageTypes.AGENT:
            raise InvalidMessageTypeError('Cannot set not_handled as True when msg is of type Agent')

        return True

    async def send(self):
        await self.check()
        result = await self._send()
        return result.get('message_id')
