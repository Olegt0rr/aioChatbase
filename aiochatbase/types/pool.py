import asyncio
import logging

logger = logging.getLogger(f'chatbase.{__name__}')


class Pool:
    def __init__(self, cb, size=5):
        """
        :param cb:
        :type cb: Chatbase
        :param size:
        :type size: int
        """
        self.messages = []
        self.size = size
        self.cb = cb
        self.task: asyncio.Future = asyncio.ensure_future(self.run())

    async def run(self):
        while True:
            if len(self.messages) >= self.size:
                await self.send_messages()
            await asyncio.sleep(2)

    async def add_message(self, msg):
        self.messages.append(msg)

    async def send_messages(self):
        message_list = self.messages.copy()
        for msg in message_list:
            self.messages.remove(msg)
        await self.cb.register_messages(message_list, task=True)

    async def close(self):
        if not self.task.cancelled():
            self.task.cancel()

        if self.messages:
            await self.send_messages()
