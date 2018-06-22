import asyncio

from aiochatbase import Chatbase

API_KEY = 'paste-your-api-key-token-here'
PLATFORM = 'Telegram'

loop = asyncio.get_event_loop()
cb = Chatbase(api_key=API_KEY, platform=PLATFORM)


async def send_messages():
    msg_1 = await cb.prepare_message('123456', 'test bulk')
    msg_2 = await cb.prepare_message('987654', 'test bulk')
    msg_3 = await cb.prepare_message('102938', 'test bulk')

    messages_list = [msg_1, msg_2, msg_3]

    result = await cb.register_messages(messages_list)
    print(f'Registered messages with ids: {result}.')


loop.run_until_complete(send_messages())
loop.close()
