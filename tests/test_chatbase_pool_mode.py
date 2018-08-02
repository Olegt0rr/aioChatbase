import pytest
import logging
import asyncio
from aiochatbase import Chatbase
from aiochatbase import types
from . import FakeChatbaseServer, BULK_RESPONSE_DICT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TrueModerTest')

pytestmark = pytest.mark.asyncio

CHATBASE_TOKEN = '123456789:AABBCCDDEEFFaabbccddeeff-1234567890'
CHATBOT_PLATFORM = 'TestPlatform'
USER_ID = '123456'
INTENT = 'Another message'
CB_MESSAGE_ID = '12345'


@pytest.yield_fixture
def cb(event_loop: asyncio.AbstractEventLoop):
    """ Chatbase fixture with pool mode """
    _chatbase = Chatbase(CHATBASE_TOKEN, CHATBOT_PLATFORM, loop=event_loop, pool_size=5)
    yield _chatbase
    event_loop.run_until_complete(_chatbase.close())


async def test_prepare_message(cb: Chatbase, event_loop):
    msg = await cb.prepare_message(user_id=USER_ID, intent=INTENT)
    assert isinstance(msg, types.Message)
    assert msg.user_id == USER_ID
    assert msg.intent == INTENT


async def test_register_message(cb: Chatbase, event_loop):
    """ Registering message in pool mode """

    assert bool(cb.pool_size)
    assert isinstance(cb.pool, types.Pool)

    async with FakeChatbaseServer(message_dict=BULK_RESPONSE_DICT, loop=event_loop):
        await cb.register_message(user_id=USER_ID, intent=INTENT)
        msg: types.Message = cb.pool.messages[0]
        assert msg.user_id == USER_ID
        assert msg.intent == INTENT

        await cb.register_message(user_id=USER_ID, intent=INTENT)
        await cb.register_message(user_id=USER_ID, intent=INTENT)
        await cb.register_message(user_id=USER_ID, intent=INTENT)
        await cb.register_message(user_id=USER_ID, intent=INTENT)
        await asyncio.sleep(3)
        assert len(cb.pool.messages) == 0


async def test_register_message_without_task(cb: Chatbase, event_loop):
    """ Registering message in pool mode without task """

    assert bool(cb.pool_size)
    assert isinstance(cb.pool, types.Pool)

    async with FakeChatbaseServer(message_dict=BULK_RESPONSE_DICT, loop=event_loop):
        await cb.register_message(user_id=USER_ID, intent=INTENT, task=False)
        msg: types.Message = cb.pool.messages[0]
        assert msg.user_id == USER_ID
        assert msg.intent == INTENT

        await cb.register_message(user_id=USER_ID, intent=INTENT, task=False)
        await cb.register_message(user_id=USER_ID, intent=INTENT, task=False)
        await cb.register_message(user_id=USER_ID, intent=INTENT, task=False)
        await cb.register_message(user_id=USER_ID, intent=INTENT, task=False)
        await asyncio.sleep(3)
        assert len(cb.pool.messages) == 0


async def test_register_message_with_task(cb: Chatbase, event_loop):
    """ Registering message in pool mode """

    assert bool(cb.pool_size)
    assert isinstance(cb.pool, types.Pool)

    async with FakeChatbaseServer(message_dict=BULK_RESPONSE_DICT, loop=event_loop):
        await cb.register_message(user_id=USER_ID, intent=INTENT, task=True)
        await asyncio.sleep(1)
        msg: types.Message = cb.pool.messages[0]
        assert msg.user_id == USER_ID
        assert msg.intent == INTENT

        await cb.register_message(user_id=USER_ID, intent=INTENT, task=True)
        await cb.register_message(user_id=USER_ID, intent=INTENT, task=True)
        await cb.register_message(user_id=USER_ID, intent=INTENT, task=True)
        await cb.register_message(user_id=USER_ID, intent=INTENT, task=True)
        await asyncio.sleep(3)
        assert len(cb.pool.messages) == 0
