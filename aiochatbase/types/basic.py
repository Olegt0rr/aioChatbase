from ..utils import json
import logging

from ..types.errors import InvalidApiKey, ChatbaseException

logger = logging.getLogger(f'chatbase.{__name__}')


class BasicChatbaseObject:
    _api_url = ''
    _content_type = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def to_json(self):
        return ''

    async def _send(self, session):
        """
        :rtype: dict
        """

        async with session.post(self._api_url, data=self.to_json(), headers=self._content_type) as resp:
            if resp.status == 200:
                response_json = await resp.text()
                response_dict = json.loads(response_json)
                logger.debug(f'Resp status: {resp.status}, resp text: {response_json}')
                return response_dict

            if resp.status == 400:
                response_json = await resp.text()
                response_dict = json.loads(response_json)
                error_text = response_dict.get('reason')

                if error_text == "Error fetching parameter 'api_key': Missing or invalid field(s): 'api_key'":
                    raise InvalidApiKey()

                raise ChatbaseException(error_text)

            raise ChatbaseException('Unknown response')
