import asyncio

from aiochatbase import Chatbase

API_KEY = 'paste-your-api-key-token-here'
PLATFORM = 'Telegram'

loop = asyncio.get_event_loop()
cb = Chatbase(api_key=API_KEY, platform=PLATFORM)


async def send_event():
    any_dict = {
        'property 1 (int)': 1,
        'property 2 (str)': 'two',
        'property 3 (float)': 3.0,
        'property 4 (bool)': True,
    }
    result = await cb.register_event('123456', 'test event', properties=any_dict)
    print(f'Event received by Chatbase? {result}!')


loop.run_until_complete(send_event())
loop.run_until_complete(cb.close())
loop.close()
