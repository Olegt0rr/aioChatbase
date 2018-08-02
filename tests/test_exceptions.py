import pytest
import logging
import asyncio
from aiochatbase import Chatbase
from aiochatbase import types
from aiochatbase.types.errors import *
from . import FakeChatbaseServer, BULK_RESPONSE_DICT, BULK_BAD_RESPONSE_DICT

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
    """
    :param event_loop:
    :rtype: Chatbase
    """
    _chatbase = Chatbase(CHATBASE_TOKEN, CHATBOT_PLATFORM, loop=event_loop)
    yield _chatbase
    event_loop.run_until_complete(_chatbase.close())


async def test_message_with_wrong_type(cb, event_loop):
    with pytest.raises(InvalidMessageTypeError):
        msg = await cb.prepare_message(user_id=USER_ID, intent=INTENT, message_type='agent007')
        await msg.check()


async def test_not_handled_agent_message(cb, event_loop):
    with pytest.raises(NotHandledAgentMessage):
        msg = await cb.prepare_message(user_id=USER_ID, not_handled=True, message_type=types.MessageTypes.AGENT)
        await msg.check()


async def test_intent_in_agent_message(cb, event_loop):
    with pytest.raises(IntentInAgentMessage):
        msg = await cb.prepare_message(user_id=USER_ID, intent='/start', message_type=types.MessageTypes.AGENT)
        await msg.check()


async def test_prepare_long_message(cb, event_loop):
    text = 'a' * 1201  # 1200 is max
    msg: types.Message = await cb.prepare_message(user_id=USER_ID, intent='/start', message=text)
    await msg.check()
    assert len(msg.message) <= 1200


async def test_register_bad_messages(cb, event_loop):
    msg_1 = await cb.prepare_message('1', 'test bulk', message=MESSAGE_TEXT)
    msg_2 = await cb.prepare_message('2', 'test bulk', not_handled=True)
    msg_3 = await cb.prepare_message('3', 'test bulk', version='Test', session_id='12345')
    messages_list = [msg_1, msg_2, msg_3]

    async with FakeChatbaseServer(message_dict=BULK_BAD_RESPONSE_DICT, loop=event_loop):
        with pytest.raises(ChatbaseException):
            await cb.register_messages(messages_list)


async def test_invalid_user_id_type(cb, event_loop):
    with pytest.raises(InvalidUserIdType):
        await cb.prepare_message(user_id=10.5, intent='/start', message_type=types.MessageTypes.AGENT)


async def test_invalid_api_token(cb, event_loop):
    reason = "Error fetching parameter 'api_key': Missing or invalid field(s): 'api_key'"
    status = 400
    async with FakeChatbaseServer(message_dict={'reason': reason, 'status': status},
                                  status=status, reason=reason, loop=event_loop):
        with pytest.raises(InvalidApiKey):
            await cb.register_message(user_id=USER_ID, intent=INTENT)


async def test_api_any_error(cb, event_loop):
    reason = "Any text"
    status = 400
    async with FakeChatbaseServer(message_dict={'reason': reason, 'status': status},
                                  status=status, reason=reason, loop=event_loop):
        with pytest.raises(ChatbaseException, message=reason):
            await cb.register_message(user_id=USER_ID, intent=INTENT)


async def test_api_unknown_response(cb, event_loop):
    reason = "Unknown response"
    status = 500
    async with FakeChatbaseServer(message_dict={'reason': reason, 'status': status},
                                  status=status, reason=reason, loop=event_loop):
        with pytest.raises(ChatbaseException, message='Unknown response'):
            await cb.register_message(user_id=USER_ID, intent=INTENT)
