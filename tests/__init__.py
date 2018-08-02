import aresponses


class FakeChatbaseServer(aresponses.ResponsesMockServer):
    def __init__(self, message_dict, status=200, reason='OK', **kwargs):
        super().__init__(**kwargs)
        self._status = status
        self._reason = reason
        self._body, self._headers = self.parse_data(message_dict)

    async def __aenter__(self):
        await super().__aenter__()
        _response = self.Response(text=self._body, headers=self._headers, status=self._status, reason=self._reason)
        self.add(self.ANY, response=_response)

    @staticmethod
    def parse_data(message_dict):
        from aiochatbase.utils import json
        _body = json.dumps(message_dict)
        _headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json; charset=utf-8',
            'X-Cloud-Trace-Context': '4b1ae036e96fa7ebc7580a046035733f',
            'Date': 'Wed, 01 Aug 2018 23:10:57 GMT',
            'Server': 'Google Frontend',
            'Content-Length': str(len(_body))
        }
        return _body, _headers


BULK_RESPONSE_DICT = {
    "all_succeeded": True,
    "responses": [
        {"message_id": 5917431215, "status": "success"},
        {"message_id": 5917431216, "status": "success"},
        {"message_id": 5917431217, "status": "success"}
    ],
    "status": 200
}

BULK_BAD_RESPONSE_DICT = {
    "all_succeeded": False,
    "responses": [
        {"message_id": 5917431215, "status": "success"},
        {"status": "failure", 'reason': "something went wrong"},
        {"message_id": 5917431217, "status": "success"}
    ],
    "status": 400
}

CLICK_RESPONSE_DICT = {"status": 200}


EVENT_RESPONSE_DICT = {
    "api_key": "123456789:AABBCCDDEEFFaabbccddeeff-1234567890",
    "creation_time": "2018-08-02T00:27:36.309320",
    "intent": "test event",
    "properties": [
        {
            "integer_value": "1",
            "property_name": "property 1 (int)"
        },
        {
            "property_name": "property 2 (str)",
            "string_value": "two"
        },
        {
            "float_value": 3.0,
            "property_name": "property 3 (float)"
        },
        {
            "integer_value": "1",
            "property_name": "property 4 (bool)",
            "semantics": "BOOLEAN"
        }
    ],
    "timestamp": "2018-08-02T00:27:35.903000",
    "user_id": "123456"
}
