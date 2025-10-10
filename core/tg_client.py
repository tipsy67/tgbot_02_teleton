import asyncio
import random

from telethon import TelegramClient
from telethon.sessions import MemorySession, StringSession

from core.config import settings
from data_app.crud.session import save_session_string, get_session_string
from data_app.schemas.session import SessionSchema


class TelegramManager:
    def __init__(self, suffix:str = ""):
        self.client: TelegramClient|None = None
        self.session_name: str = settings.tg.session + suffix
        self.session: TelegramClient|None = None
        self.lock = asyncio.Lock()
        # self.system_version = str(random.uniform(0.1, 100.9))
        self.device_suffix = suffix
        self.device_configs = {
            "": {
                "model": "iPhone 15 Pro",
                "system": "iOS 17.1.2",
                "app": "10.2.1"
            },
            "_tasks": {
                "model": "Samsung Galaxy S24",
                "system": "Android 14",
                "app": "10.1.8"
            },
            "_worker": {
                "model": "Desktop Windows",
                "system": "Windows 11",
                "app": "10.3.0"
            }
        }

    async def get_client(self):
        try:
            # async with self.lock:
            #     print("✅ Лок получен")
            if self.client is None:
                config = self.device_configs.get(self.device_suffix, self.device_configs[""])
                api_id = int(settings.tg.api_id)
                session_string = await get_session_string(api_id)
                if session_string is None:
                    session=StringSession()
                else:
                    session=StringSession(session_string)
                print("🆕 Создаем нового клиента...")
                self.client = TelegramClient(
                    session=MemorySession(),#self.session_name,
                    api_id=int(settings.tg.api_id),
                    api_hash=settings.tg.api_hash,
                    # device_model=config["model"],
                    # system_version=config["system"],
                    # app_version=config["app"]
                )
                await self.client.start()
                print(self.client.session.auth_key.key_id)
                print("✅ Клиент готов")
                if session_string is None:
                    session_string = self.client.session.save()
                    session_data = SessionSchema(
                        api_id=api_id,
                        session_string=session_string
                    )
                    await save_session_string(session_data=session_data)
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



tg_manager = TelegramManager()
tg_manager_for_task = TelegramManager(suffix="_task")