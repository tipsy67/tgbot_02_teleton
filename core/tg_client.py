import asyncio

from telethon import TelegramClient

from core.config import settings

# client = TelegramClient(settings.tg.session, int(settings.tg.api_id), settings.tg.api_hash)


class TelegramManager:
    def __init__(self):
        self.client: TelegramClient|None = None
        # self.lock = asyncio.Lock()

    async def get_client(self) ->TelegramClient:
        # async with self.lock:
        if self.client is None:
            self.client = TelegramClient(settings.tg.session, int(settings.tg.api_id), settings.tg.api_hash)
            await self.client.start()
        return self.client

    async def close(self):
        # async with self.lock:
        if self.client and self.client.is_connected():
            await self.client.disconnect()
        self.client = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


tg_manager = TelegramManager()