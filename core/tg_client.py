import asyncio
import random

from telethon import TelegramClient

from core.config import settings


class TelegramManager:
    def __init__(self, suffix:str = ""):
        self.client: TelegramClient|None = None
        self.session_name: str = settings.tg.session + suffix
        self.session: TelegramClient|None = None
        self.lock = asyncio.Lock()
        self.system_version = str(random.uniform(0.1, 100.9))

    async def get_client(self) ->TelegramClient:
        print("🔒 Пытаемся получить лок...")
        try:
            async with self.lock:
                print("✅ Лок получен")
                if self.client is None:
                    print("🆕 Создаем нового клиента...")
                    self.client = TelegramClient(
                        session=self.session_name,
                        api_id=int(settings.tg.api_id),
                        api_hash=settings.tg.api_hash,
                        system_version=self.system_version,
                    )
                    await self.client.start()
                print("✅ Клиент готов")
                return self.client
        except asyncio.CancelledError as e:
            print("❌ CANCELLED в get_client!")
            raise
        except Exception as e:
            print(f"❌ Другая ошибка в get_client: {e}")
            raise



    async def close(self):
        if self.client and self.client.is_connected():
            await self.client.disconnect()
        self.client = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


tg_manager = TelegramManager()
tg_manager_for_task = TelegramManager(suffix="_task")