import logging

from ..utils import json
from .basic import BasicChatbaseObject

logger = logging.getLogger(f'chatbase.{__name__}')


class Click(BasicChatbaseObject):
    def __init__(self, api_key, url, platform, user_id=None, version=None, session=None):
        """

        :param api_key: the Chatbase ID of the bot
        :type api_key: str

        :param url: The full URL to redirect to.
        :type url: str

        :param user_id: the id of the user who clicked the link
        :type user_id: str

        :param platform: valid values "Facebook", "SMS", "Web", "Android", "iOS", "Actions", "Alexa", "Cortana", "Kik",
                            "Skype", "Twitter", "Viber", "Telegram", "Slack", "WhatsApp", "WeChat", "Line", "Kakao"
                            or a custom name like "Workplace" or "OurPlatform"
        :type platform: str

        :param version: set for user and bot messages the version of the bot processing the message
        :type version: str

        """
        # aiohttp
        self.session = session

        # required
        self.api_key = api_key
        self.url = url
        self.platform = platform

        # optional
        self.user_id = str(user_id) if user_id else None
        self.version = str(version) if version else None

        self._api_url = f"https://chatbase.com/api/click"

    def to_json(self):
        """ Return a JSON version for use with the Chatbase API """

        data = {
            'api_key': self.api_key,
            'url': self.url,
            'platform': self.platform,
            'user_id': self.user_id or '',
            'version': self.version or '',
        }
        return json.dumps(data)

    async def send(self):
        result = await self._send(self.session)
        if result.get('status') == 200:
            return True
