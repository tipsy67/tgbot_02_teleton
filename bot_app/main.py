import asyncio
import logging

from telethon import events, TelegramClient

from core.config import settings
from core.taskiq_broker import broker
from core.tg_client import tg_managers, TelegramManager
from bot_app.tasks import process_and_reply, initial_client
from data_app.crud.channel import get_users_channels, get_id_users_channels
from data_app.crud.user import get_active_users
from data_app.models import ChannelModel

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


log = logging.getLogger(__name__)


async def initial_clients():
    tg_manager_for_worker = tg_managers["worker"]
    users = await get_active_users()
    for user in users:
        client = await tg_manager_for_worker.get_client(user.phone_number)
        # log.info(await TelegramManager.get_user_chats(client))
        await tg_manager_for_worker.close_client(user.phone_number)
        task = await initial_client.kiq(user.id, user.phone_number)

async def main():
    try:
        await broker.startup()
        await initial_clients()
    except KeyboardInterrupt:
        log.info("Stopped by user")
    finally:
        await broker.shutdown()
        log.info("Main script done")


if __name__ == "__main__":
    asyncio.run(main())
