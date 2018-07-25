import logging
from typing import List

from .basic import BasicChatbaseObject
from .property import Property
from ..utils import json

logger = logging.getLogger(f'chatbase.{__name__}')


class Event(BasicChatbaseObject):
    def __init__(self, api_key, user_id, intent, timestamp_millis=None, platform=None, version=None, properties=None,
                 session=None):
        """

        :param api_key:
        :param user_id:
        :param intent:
        :param timestamp_millis:
        :param platform:
        :param version:
        :param properties: Event properties in dict format
        :type properties: dict
        """
        # aiohttp
        self.session = session

        # required
        self.api_key = api_key
        self.user_id = str(user_id)
        self.intent = intent

        # optional
        self.timestamp_millis = timestamp_millis
        self.platform = platform
        self.version = version
        self.properties: List[Property] = [Property(k, v) for k, v in properties.items()]

        self._api_url = f"https://api.chatbase.com/apis/v1/events/insert"

    def to_json(self):
        """ Return a JSON version for use with the Chatbase API """

        data = {
            'api_key': self.api_key,
            'user_id': self.user_id,
            'intent': self.intent,
        }

        if self.timestamp_millis:
            data['timestamp_millis'] = self.timestamp_millis

        if self.platform:
            data['platform'] = self.platform

        if self.version:
            data['version'] = self.version

        if self.properties:
            data['properties'] = [p() for p in self.properties]

        return json.dumps(data)

    async def send(self):
        result = await self._send(session=self.session)
        if result.get('creation_time'):
            return True
