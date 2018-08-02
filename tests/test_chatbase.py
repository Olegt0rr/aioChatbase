import pytest
import logging
import asyncio
from aiochatbase import Chatbase
from aiochatbase import types
from . import FakeChatbaseServer, CLICK_RESPONSE_DICT, BULK_RESPONSE_DICT, EVENT_RESPONSE_DICT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TrueModerTest')

pytestmark = pytest.mark.asyncio

CHATBASE_TOKEN = '123456789:AABBCCDDEEFFaabbccddeeff-1234567890'
CHATBOT_PLATFORM = 'TestPlatform'
USER_ID = '123456'
MESSAGE_TEXT = 'test message text'
INTENT = 'Another message'
CB_MESSAGE_ID = '12345'


@pytest.yield_fixture
def cb(event_loop: asyncio.AbstractEventLoop):
    _chatbase = Chatbase(CHATBASE_TOKEN, CHATBOT_PLATFORM, loop=event_loop)
    yield _chatbase
    event_loop.run_until_complete(_chatbase.close())


async def test_cb_init_without_loop(event_loop):
    chatbase = Chatbase(CHATBASE_TOKEN, CHATBOT_PLATFORM)
    await chatbase.close()


async def test_prepare_message(cb, event_loop):
    msg = await cb.prepare_message(user_id=USER_ID, intent=INTENT, message=MESSAGE_TEXT)
    assert isinstance(msg, types.Message)
    assert msg.user_id == USER_ID
    assert msg.intent == INTENT
    assert msg.message == MESSAGE_TEXT


async def test_register_message(cb, event_loop):
    """ Registering message in basic mode """

    async with FakeChatbaseServer(message_dict={'message_id': CB_MESSAGE_ID, 'status': 200}, loop=event_loop):
        result = await cb.register_message(user_id=USER_ID, intent=INTENT)
        assert result == CB_MESSAGE_ID


async def test_register_message_without_task(cb, event_loop):
    """ Registering message in basic mode strongly without task """

    async with FakeChatbaseServer(message_dict={'message_id': CB_MESSAGE_ID, 'status': 200}, loop=event_loop):
        result = await cb.register_message(user_id=USER_ID, intent=INTENT, task=False)
        assert result == CB_MESSAGE_ID


async def test_register_message_with_task(cb, event_loop):
    """ Registering message in basic mode with task """
    async with FakeChatbaseServer(message_dict={'message_id': CB_MESSAGE_ID, 'status': 200}, loop=event_loop):
        result = await cb.register_message(user_id=USER_ID, intent=INTENT, task=True)
        assert isinstance(result, asyncio.Task)
        done, pending = await asyncio.wait([result], return_when=asyncio.ALL_COMPLETED)
        assert done.pop().result() == CB_MESSAGE_ID


async def test_register_messages(cb, event_loop):
    msg_1 = await cb.prepare_message('1', 'test bulk', message=MESSAGE_TEXT)
    msg_2 = await cb.prepare_message('2', 'test bulk', not_handled=True)
    msg_3 = await cb.prepare_message('3', 'test bulk', version='Test', session_id='12345')
    messages_list = [msg_1, msg_2, msg_3]

    async with FakeChatbaseServer(message_dict=BULK_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_messages(messages_list)
        assert result == [5917431215, 5917431216, 5917431217]


async def test_register_messages_without_task(cb, event_loop):
    msg_1 = await cb.prepare_message('1', 'test bulk')
    msg_2 = await cb.prepare_message('2', 'test bulk')
    msg_3 = await cb.prepare_message('3', 'test bulk')
    messages_list = [msg_1, msg_2, msg_3]
    async with FakeChatbaseServer(message_dict=BULK_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_messages(messages_list, task=False)
        assert result == [5917431215, 5917431216, 5917431217]


async def test_register_messages_with_task(cb, event_loop):
    msg_1 = await cb.prepare_message('1', 'test bulk')
    msg_2 = await cb.prepare_message('2', 'test bulk')
    msg_3 = await cb.prepare_message('3', 'test bulk')
    messages_list = [msg_1, msg_2, msg_3]

    async with FakeChatbaseServer(message_dict=BULK_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_messages(messages_list, task=True)
        assert isinstance(result, asyncio.Task)
        done, pending = await asyncio.wait([result], return_when=asyncio.ALL_COMPLETED)
        assert done.pop().result() == [5917431215, 5917431216, 5917431217]


async def test_register_click(cb, event_loop):
    async with FakeChatbaseServer(message_dict=CLICK_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_click(url='google.com')
    assert result is True


async def test_register_click_without_task(cb, event_loop):
    async with FakeChatbaseServer(message_dict=CLICK_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_click(url='google.com', task=False)
    assert result is True


async def test_register_click_with_task(cb, event_loop):
    async with FakeChatbaseServer(message_dict=CLICK_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_click(url='google.com', task=True)
        assert isinstance(result, asyncio.Task)
        done, pending = await asyncio.wait([result], return_when=asyncio.ALL_COMPLETED)
        assert done.pop().result() is True


async def test_register_event(cb, event_loop):
    any_dict = {
        'property 1 (int)': 1,
        'property 2 (str)': 'two',
        'property 3 (float)': 3.0,
        'property 4 (bool)': True,
    }
    async with FakeChatbaseServer(message_dict=EVENT_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_event('123456', 'test event', properties=any_dict, version='TestVersion')
    assert result is True


async def test_register_event_without_task(cb, event_loop):
    any_dict = {
        'property 1 (int)': 1,
        'property 2 (str)': 'two',
        'property 3 (float)': 3.0,
        'property 4 (bool)': True,
    }
    async with FakeChatbaseServer(message_dict=EVENT_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_event('123456', 'test event', properties=any_dict, task=False)
    assert result is True


async def test_register_event_with_task(cb, event_loop):
    any_dict = {
        'property 1 (int)': 1,
        'property 2 (str)': 'two',
        'property 3 (float)': 3.0,
        'property 4 (bool)': True,
    }
    async with FakeChatbaseServer(message_dict=EVENT_RESPONSE_DICT, loop=event_loop):
        result = await cb.register_event('123456', 'test event', properties=any_dict, task=True)
        assert isinstance(result, asyncio.Task)
        done, pending = await asyncio.wait([result], return_when=asyncio.ALL_COMPLETED)
        assert done.pop().result() is True
