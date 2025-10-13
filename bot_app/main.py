import asyncio
import logging

from telethon import events, TelegramClient

from core.config import settings
from core.taskiq_broker import broker
from core.tg_client import tg_managers, TelegramManager
from bot_app.tasks import process_and_reply
from data_app.crud.channel import get_users_channels, get_id_users_channels
from data_app.crud.user import get_active_users
from data_app.models import ChannelModel

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


log = logging.getLogger(__name__)
#
# @broker.on_result
# async def send_reply(result):
#     data = result.return_value
#     if data:
#         await reply_to_message(
#             chat_id=data["chat_id"],
#             message_id=data["message_id"],
#             reply_text=data["content"]
#         )


async def register_tg_handler(phone_number, client: TelegramClient, chats: list[ChannelModel]):
    @client.on(events.NewMessage(chats=chats))
    async def message_handler(event):
        if event.chat_id in chats and not event.message.out:
            try:
                result = await process_and_reply.kiq(
                    phone_number=phone_number,
                    chat_id=event.chat_id,
                    message_id=event.message.id,
                    original_text=event.message.text,
                )
                log.info("Sent to broker: %s", result)
            except Exception as e:
                log.error("Broker error: %s", e)

async def initial_clients():
    users = await get_active_users()
    tg_manager_for_handlers = tg_managers["handler"]
    tg_manager_for_worker = tg_managers["worker"]
    for user in users:
        client = await tg_manager_for_handlers.get_client(user.phone_number)
        # print(await TelegramManager.get_user_chats(client))
        chats = await get_id_users_channels(user)
        await register_tg_handler(user.phone_number, client, chats)

        await tg_manager_for_worker.get_client(user.phone_number)
    await tg_manager_for_worker.close_all_clients()

async def main():
    try:
        await broker.startup()

        await initial_clients()

        await asyncio.gather(*[client.run_until_disconnected() for client in tg_managers["handler"]._clients.values()])

    except KeyboardInterrupt:
        log.debug("Stopped by user")
    finally:
        await tg_managers["handler"].close_all_clients()
        await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
