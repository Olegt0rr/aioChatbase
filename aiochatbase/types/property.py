import logging

logger = logging.getLogger(f'chatbase.{__name__}')


class Property:
    def __init__(self, name, value):
        """

        :param name: The name of the property.
        :type name: str

        :param value: A tag to attach to the event.

        """
        # required
        self.name = name
        self.value = value

        self._content_type = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self._api_url = f"https://api.chatbase.com/apis/v1/events/insert"

    def __call__(self, *args, **kwargs):
        return self.to_dict()

    def to_dict(self):
        """ Return a dict version for use with the Chatbase API """

        data = {
            'property_name': self.name,
        }
        if isinstance(self.value, str):
            data['string_value'] = self.value

        if isinstance(self.value, int):
            data['integer_value'] = self.value

        if isinstance(self.value, float):
            data['float_value'] = self.value

        if isinstance(self.value, bool):
            data['bool_value'] = self.value

        return data
