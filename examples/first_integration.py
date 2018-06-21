import asyncio

from aiochatbase import Chatbase

API_KEY = 'paste-your-api-key-token-here'
API_KEY = '94735589-03f9-450c-9666-66cd2efdf21e'
PLATFORM = 'Telegram'

loop = asyncio.get_event_loop()
cb = Chatbase(api_key=API_KEY, platform=PLATFORM)


async def send_handled_message():
    result = await cb.register_message(user_id='123456', intent='test message')
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

    if len(done) != len(tasks):

        # get exception reason
        for task in done:
            print(f'ERROR! {task.exception()}')

        # cancel other tasks
        for task in pending:
            task.cancel()

        print('=== Integration NOT completed ===')
        return

    print('=== Integration completed ===')


loop.run_until_complete(integration())
loop.close()
