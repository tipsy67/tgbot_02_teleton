import asyncio

from telethon import events, TelegramClient

from core.taskiq_broker import broker
from core.tg_client import tg_manager
from bot_app.tasks import process_and_reply

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
                print(f"✅ Sent to broker: {result}")
            except Exception as e:
                print(f"❌ Broker error: {e}")



async def main():
    try:
        await broker.startup()

        client = await tg_manager.get_client()

        await register_tg_handler(client)

        await client.run_until_disconnected()

    except KeyboardInterrupt:
        print("\n🛑 Stopped")
    finally:
        await tg_manager.close()
        await broker.shutdown()


if __name__ == '__main__':
    asyncio.run(main())