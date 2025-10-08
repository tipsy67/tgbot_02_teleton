import asyncio

from telethon import events

from core.tg_client import TelegramManager, tg_manager
from bot_app.tasks import process_and_reply
from core.taskiq_broker import broker




async def simple_monitor():
    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)
    client = await tg_manager.get_client()
    @client.on(events.NewMessage(chats=-4921301938))
    async def message_handler(event):
        if not event.message.out:
            await process_and_reply.kiq(
                chat_id=-4921301938,
                message_id=event.message.id,
                original_text=event.message.text
            )



async def main():
    client = await tg_manager.get_client()
    await broker.startup()

    await simple_monitor()
    print("🚀 Бот запущен и слушает сообщения...")
    print("⏹️  Для остановки нажмите Ctrl+C")

    await client.run_until_disconnected()
    await tg_manager.close()
    await broker.shutdown()


if __name__ == '__main__':
    asyncio.run(main())