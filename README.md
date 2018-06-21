# aioChatbase 
[![Supported python versions](https://img.shields.io/pypi/pyversions/aiogram.svg?style=flat-square)](https://pypi.python.org/pypi/aiogram)
[![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![PyPi Package Version](https://img.shields.io/pypi/v/aioChatbase.svg?style=flat-square)](https://pypi.python.org/pypi/aioChatbase)
[![PyPi status](https://img.shields.io/pypi/status/aioChatbase.svg?style=flat-square)](https://pypi.python.org/pypi/aioChatbase)

**aioChatbase** is a library for [Chatbase Generic Message API](https://chatbase.com/documentation/generic) written in Python 3.6 with [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://github.com/aio-libs/aiohttp). 
It helps to integrate Chatbase with your chatbot.

## How to install
```
python3.6 -m pip install aioChatbase
```

## How to use
1) Import Chatbase
```python
from aiochatbase import Chatbase
```

2) Create cb instance
```python
cb = Chatbase(API_KEY, BOT_PLATFORM)
```

3) Register handled message
```python
await cb.register_message(user_id='123456', intent='start')
```

4) Register non-handled message
```python
await cb.register_message(user_id='123456', intent='unknown message', not_handled=True)
```

5) Register url click
```python
await cb.register_click(url='google.com')
```

 Check more examples at /examples folder
