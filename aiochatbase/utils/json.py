"""
ujson support module

"""

import json

try:
    import ujson

except ImportError:  # pragma: no cover
    ujson = None

_use_ujson = True if ujson else False


def disable_ujson():  # pragma: no cover
    global _use_ujson
    _use_ujson = False


def dumps(data):
    global _use_ujson
    if _use_ujson:
        return ujson.dumps(data)
    return json.dumps(data)


def loads(data):
    global _use_ujson
    if _use_ujson:
        return ujson.loads(data)
    return json.loads(data)
