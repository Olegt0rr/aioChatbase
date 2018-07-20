import asyncio

from aiochatbase import Chatbase

API_KEY = 'paste-your-api-key-token-here'
PLATFORM = 'Telegram'

loop = asyncio.get_event_loop()
cb = Chatbase(api_key=API_KEY, platform=PLATFORM)


async def send_handled_message():
    result = await cb.register_message(user_id='512345678', intent='test message 2')
    print(f'Handled Chatbase message id: {result}')


async def send_non_handled_message():
    result = await cb.register_message(user_id='123456', intent='another test message', not_handled=True)
    print(f'non handled Chatbase message id: {result}')


async def send_url_click():
    result = await cb.register_click(url='google.com')
    print(f'Is click registered? {result}!')


async def integration():
    print('=== Integration started ===')
    tasks = [
        send_handled_message(),
        send_non_handled_message(),
        send_url_click(),
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

    # get exception reason
    for task in done:
        if task.exception():
            print(f'ERROR! {task.exception()}')

            # cancel other tasks
            for t in pending:
                t.cancel()
            print('=== Integration NOT completed ===')
            return

    print('=== Integration completed ===')


loop.run_until_complete(integration())
loop.run_until_complete(cb.close())
loop.close()
