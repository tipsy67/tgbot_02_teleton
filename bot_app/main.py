import asyncio
import logging

from telethon import events, TelegramClient

from core.config import settings
from core.taskiq_broker import broker
from core.tg_client import tg_manager, tg_manager_for_task
from bot_app.tasks import process_and_reply



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

async def register_tg_handler(client: TelegramClient):
    @client.on(events.NewMessage(chats=-4921301938))
    async def message_handler(event):
        if event.chat_id == -4921301938 and not event.message.out:
            try:
                result = await process_and_reply.kiq(
                    chat_id=-4921301938,
                    message_id=event.message.id,
                    original_text=event.message.text
                )
                log.info("Sent to broker: %s" ,result)
            except Exception as e:
                log.error("Broker error: %s", e)



async def main():
    try:
        await broker.startup()

        client = await tg_manager.get_client()

        await tg_manager_for_task.get_client()
        await tg_manager_for_task.close()

        await register_tg_handler(client)

        await client.run_until_disconnected()

    except KeyboardInterrupt:
        log.debug("Stopped by user")
    finally:
        await tg_manager.close()
        await broker.shutdown()


if __name__ == '__main__':
    asyncio.run(main())