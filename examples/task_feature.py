import asyncio

from aiochatbase import Chatbase

API_KEY = 'paste-your-api-key-token-here'
PLATFORM = 'Telegram'

loop = asyncio.get_event_loop()
cb = Chatbase(api_key=API_KEY, platform=PLATFORM, task_mode=True, loop=loop)


async def background_send_handled_message():
    print('Registering message as background task...')
    task: asyncio.Task = await cb.register_message(user_id='512345678', intent='test message 2')

    print("Let's calc 2+2, while cb registering message...")
    s = 2 + 2
    print(f'2 + 2 = {s}')
    await asyncio.sleep(2)

    print(f"Let's get Chatbase message id: {task.result()}")


loop.run_until_complete(background_send_handled_message())
loop.run_until_complete(cb.close())
loop.close()
