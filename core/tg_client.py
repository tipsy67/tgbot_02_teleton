import asyncio
import logging
from typing import Optional

from telethon import TelegramClient
from telethon.sessions import StringSession

from core.config import settings
from data_app.crud.session import save_session_string, get_session_string
from data_app.schemas.session import SessionSchema

logger = logging.getLogger(__name__)


class TelegramManager:
    def __init__(self, suffix: str = ""):
        self.client: Optional[TelegramClient] = None
        self.session_name: str = settings.tg.session + suffix
        self.lock = asyncio.Lock()
        self.device_suffix = suffix
        logger.info("Инициализирован TelegramManager с суффиксом: %s ", suffix)

    async def get_client(self) -> TelegramClient:
        """Получить клиент Telegram, создавая новый при необходимости."""
        try:
            if self.client is not None and self.client.is_connected():
                logger.info("Возвращаем существующий подключенный клиент с суффиксом: %s ", self.device_suffix)
                return self.client

            logger.info("Создание нового клиента Telegram с суффиксом: %s ", self.device_suffix)
            session_data = SessionSchema(
                api_id=int(settings.tg.api_id),
                session_string="",
                suffix=self.device_suffix
            )

            session_string = await get_session_string(session_data)
            if session_string:
                logger.info("Найдена сохраненная сессия в базе данных")
                session = StringSession(session_string)
            else:
                logger.info("Создана новая сессия")
                session = StringSession()

            self.client = TelegramClient(
                session=session,
                api_id=int(settings.tg.api_id),
                api_hash=settings.tg.api_hash,
            )

            logger.debug("Запускаем клиент Telegram с суффиксом: %s ...", self.device_suffix)
            await self.client.start()

            if hasattr(self.client.session, 'auth_key') and self.client.session.auth_key:
                logger.info(f"Клиент авторизован, key_id: {self.client.session.auth_key.key_id}")

            if not session_string:
                new_session_string = self.client.session.save()
                session_data.session_string = new_session_string
                await save_session_string(session_data=session_data)
                logger.info("Новая сессия сохранена в базу данных")

            logger.info("Клиент Telegram успешно инициализирован с суффиксом: %s ...", self.device_suffix)
            return self.client

        except asyncio.CancelledError:
            logger.error("Операция получения клиента была прервана")
            raise
        except Exception as e:
            logger.error("Критическая ошибка при инициализации клиента Telegram: %s", e, exc_info=True)
            raise

    async def close(self):
        """Корректно закрыть соединение с Telegram."""
        try:
            if self.client:
                if self.client.is_connected():
                    logger.info("Завершаем соединение с Telegram с суффиксом: %s ...", self.device_suffix)
                    await self.client.disconnect()
                    logger.info("Соединение с Telegram закрыто")
                self.client = None
        except Exception as e:
            logger.error("Ошибка при закрытии клиента Telegram: %s", e, exc_info=True)

    async def __aenter__(self):
        """Поддержка контекстного менеджера."""
        return await self.get_client()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие при выходе из контекста."""
        await self.close()


# Создаем экземпляры менеджеров
tg_manager = TelegramManager()
tg_manager_for_task = TelegramManager(suffix="_task")