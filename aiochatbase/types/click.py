import json
import logging

import aiohttp

from ..types.errors import ReceivedNoMessage, ChatbaseException, InvalidApiKey

logger = logging.getLogger(f'chatbase.{__name__}')


class Click:
    def __init__(self, api_key, url, platform, user_id=None, version=None):
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
        # required
        self.api_key = api_key
        self.url = url
        self.platform = platform

        # optional
        self.user_id = user_id
        self.version = version

        self._content_type = {'Content-type': 'application/json', 'Accept': 'text/plain'}
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
        """ Send the message set to the Chatbase API """

        async with aiohttp.ClientSession() as session:
            async with session.post(self._api_url, data=self.to_json(), headers=self._content_type) as resp:
                if resp.status == 200:
                    response_json = await resp.text()
                    logger.debug(f'Resp status: {resp.status}, resp text: {response_json}')
                    return True

                if resp.status == 400:
                    response_json = await resp.text()
                    response_dict = json.loads(response_json)
                    error_text = response_dict.get('reason')

                    if error_text == "Error fetching parameter 'api_key': Missing or invalid field(s): 'api_key'":
                        raise InvalidApiKey()

                    raise ChatbaseException(error_text)

                raise ChatbaseException('Unknown response')
