from aiochatbase.utils import json


def test_disable_json():
    json.disable_ujson()
    # json._use_ujson = False
    d = {}
    result = json.dumps(d)
    assert result == '{}'

    d = json.loads(result)
    assert d == {}
