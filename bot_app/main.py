import asyncio

from telethon import events

from core.tg_client import TelegramManager, tg_manager
from bot_app.tasks import process_and_reply
from core.taskiq_broker import broker




async def simple_monitor(client_tg):
    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)
    @client_tg.on(events.NewMessage(chats=-4921301938))
    async def message_handler(event):
        print("event")
        if not event.message.out:
            print("event after")
            await process_and_reply.kiq(
                chat_id=-4921301938,
                message_id=event.message.id,
                original_text=event.message.text
            )


async def main():
    try:
        await broker.startup()
        print("✅ Брокер запущен")
        client = await tg_manager.get_client()
        print("✅ Основной клиент готов")

        # ✅ ОБРАБОТЧИК ДЛЯ ВСЕХ СООБЩЕНИЙ (для отладки)
        @client.on(events.NewMessage)
        async def all_messages_handler(event):
            print(f"\n🔍 ВСЕ СООБЩЕНИЯ:")
            print(f"   Чат ID: {event.chat_id}")
            print(f"   Текст: {event.message.text}")
            print(f"   Out: {event.message.out}")

            # Фильтруем по нужному чату
            if event.chat_id == -4921301938:
                print("🎯 ЭТО НАШ ЧАТ!")

                if not event.message.out:
                    print("🔄 Обрабатываем входящее сообщение...")
                    try:

                        result = await process_and_reply.kiq(
                            chat_id=-4921301938,
                            message_id=event.message.id,
                            original_text=event.message.text
                        )
                        print(f"✅ Задача отправлена в брокер: {result}")
                    except Exception as e:
                        print(f"❌ Ошибка брокера: {e}")

        print("✅ Универсальный обработчик зарегистрирован")

        # Проверка доступа к чату
        try:
            chat = await client.get_entity(-4921301938)
            print(f"✅ Доступ к чату есть: {chat.title}")
        except Exception as e:
            print(f"❌ Ошибка доступа к чату: {e}")

        print("🚀 Бот запущен...")
        await client.run_until_disconnected()

    except KeyboardInterrupt:
        print("\n🛑 Остановка...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await tg_manager.close()
        await broker.shutdown()


if __name__ == '__main__':
    asyncio.run(main())