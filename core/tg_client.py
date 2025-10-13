import asyncio
import logging

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneNumberInvalidError, PhoneCodeInvalidError, \
    PhoneCodeExpiredError
from telethon.sessions import StringSession

from core.config import settings
from data_app.crud.session import save_session_string, get_session_string
from data_app.schemas.session import SessionSchema

log = logging.getLogger(__name__)


class TelegramManager:
    def __init__(self, _suffix:str = ""):
        self._clients: dict[str, TelegramClient] = {}
        self._suffix = _suffix
        log.info("Инициализирован TelegramManager")


    async def get_client(self, phone_number:str) -> TelegramClient:
        client = await self.init_client(phone_number)

        if client and not await client.is_user_authorized():
            client = await self.authenticate_client(phone_number, client)

        return client


    async def init_client(self, phone_number:str) -> TelegramClient:
        """Получить клиент Telegram, создавая новый при необходимости."""
        try:
            name = phone_number + "_" + self._suffix
            if name in self._clients:
                client = self._clients[name]
                if client is not None and client.is_connected():
                    log.info(
                        "Возвращаем существующий подключенный клиент: %s ",
                        name,
                    )
                    return client

            log.info(
                "Создание нового клиента Telegram: %s ", name
            )

            session_data = SessionSchema(
                phone_number=phone_number,
                session_string="",
                suffix=self._suffix,
            )

            session_string = await get_session_string(session_data)
            if session_string:
                log.info("Найдена сохраненная сессия в базе данных")
                session = StringSession(session_string)
            else:
                log.info("Создана новая сессия")
                session = StringSession()

            client = TelegramClient(
                session=session,
                api_id=int(settings.tg.api_id),
                api_hash=settings.tg.api_hash,
            )
            self._clients[name] = client
            await client.connect()
            return client

        except asyncio.CancelledError:
            log.error("Операция получения клиента была прервана")
            raise
        except Exception as e:
            log.error(
                "Критическая ошибка при инициализации клиента Telegram: %s",
                e,
                exc_info=True,
            )
            raise

    async def authenticate_client(self, phone_number: str, client: TelegramClient) -> TelegramClient:
        """Аутентификация клиента по номеру телефона."""
        try:
            log.info("Начало аутентификации для %s", phone_number)

            if await client.is_user_authorized():
                log.info("Клиент уже авторизован для %s", phone_number)
                return client

            # Отправляем код подтверждения
            await client.send_code_request(phone_number)
            log.info("Код подтверждения отправлен на %s", phone_number)

            # Запрашиваем код у пользователя
            code = await self._get_verification_code(phone_number)

            if not code:
                raise ValueError("Код подтверждения не получен")

            # Пытаемся войти с кодом
            try:
                await client.sign_in(phone_number, code)
                log.info("Успешная аутентификация для %s", phone_number)

            except SessionPasswordNeededError:
                log.info("Требуется пароль двухфакторной аутентификации для %s", phone_number)
                password = await self._get_2fa_password(phone_number)
                await client.sign_in(password=password)
                log.info("Успешная аутентификация с 2FA для %s", phone_number)

            except PhoneNumberInvalidError:
                log.error("Неверный номер телефона: %s", phone_number)
                raise
            except PhoneCodeInvalidError:
                log.error("Неверный код подтверждения для %s", phone_number)
                raise
            except PhoneCodeExpiredError:
                log.error("Срок действия кода истек для %s", phone_number)
                raise

            # Сохраняем session_string в базу данных
            session_string = client.session.save()
            await self._save_session_string(phone_number, session_string)
            log.info("Сессия сохранена в базу данных для %s", phone_number)

            return client

        except Exception as e:
            log.error(
                "Ошибка аутентификации для %s: %s",
                phone_number,
                e,
                exc_info=True
            )
            await client.disconnect()
            raise

    async def _get_verification_code(self, phone_number: str) -> str:
        """Получить код подтверждения от пользователя."""
        code = input(f"Введите код подтверждения для {phone_number}: ").strip()
        return code


    async def _get_2fa_password(self, phone_number: str) -> str:
        """Получить пароль двухфакторной аутентификации."""
        password = input(f"Введите пароль двухфакторной аутентификации для {phone_number}: ").strip()
        return password

    async def _save_session_string(self, phone_number: str, session_string: str):
        """Сохранить session_string в базу данных."""
        try:
            session_data = SessionSchema(
                phone_number=phone_number,
                session_string=session_string,
                suffix=self._suffix,
            )
            await save_session_string(session_data)
        except Exception as e:
            log.error(
                "Ошибка сохранения сессии для %s: %s",
                phone_number,
                e
            )

    async def close_client(self, phone_number: str):
        """Закрыть клиент для указанного номера."""
        name = phone_number + "_" + self._suffix
        if name in self._clients:
            client = self._clients[name]
            if client and client.is_connected():
                await client.disconnect()
                log.info("Клиент отключен для %s", name)
            del self._clients[name]

    async def close_all_clients(self):
        """Закрыть все клиенты."""
        for phone_number in list(self._clients.keys()):
            await self.close_client(phone_number.replace("_" + self._suffix, ""))

    @staticmethod
    def _get_chat_type(dialog) -> str:
        """Определить тип чата"""
        if dialog.is_user:
            return "private"
        elif dialog.is_group:
            return "group"
        elif dialog.is_channel:
            return "channel"
        else:
            return "unknown"

    @staticmethod
    async def get_user_chats(client: TelegramClient) -> list:
        """Получить все чаты и диалоги пользователя"""
        try:
            chats = []
            async for dialog in client.iter_dialogs():
                chat_info = {
                    'id': dialog.id,
                    'name': dialog.name,
                    'type': TelegramManager._get_chat_type(dialog),
                    'unread_count': dialog.unread_count,
                    'unread_mentions_count': dialog.unread_mentions_count,
                    'is_user': dialog.is_user,
                    'is_group': dialog.is_group,
                    'is_channel': dialog.is_channel,
                    'entity': dialog.entity
                }
                chats.append(chat_info)

            return chats

        except Exception as e:
            log.error("Ошибка получения чатов: %s", e)
            return []




# Создаем экземпляры менеджеров
tg_managers: dict[str, TelegramManager] = dict()
for suffix in settings.suffixes:
    tg_managers[suffix] = TelegramManager(suffix)