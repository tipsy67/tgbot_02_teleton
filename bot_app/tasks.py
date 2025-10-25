import asyncio
import logging
import os

from telethon import events

from bot_app.utils import generate_content
from core.taskiq_broker import broker
from core.tg_client import tg_managers
from data_app.crud.channel import get_id_users_channels, get_users_channels
import psutil



log = logging.getLogger(__name__)
tg_manager_for_worker = tg_managers["worker"]


def parse_keywords(text: str, delimiter: str = ",") -> list[str]:
    """Парсит строку с ключевыми словами в список"""
    if not text:
        return []

    return [word.strip() for word in text.split(delimiter) if word.strip()]


@broker.task
async def initial_client(user_id: int, phone_number: str):
    import psutil
    process = psutil.Process(os.getpid())

    async def background_timestamp():
        """Фоновая задача для мониторинга"""
        while True:
            memory_current = process.memory_info().rss / 1024 / 1024
            log.debug(f"⏰ BACKGROUND MONITOR {phone_number} - Memory: {memory_current:.2f} MB")
            await asyncio.sleep(120)

    async def register_tg_handler():
        log.info("register handler %s %s", user_id, phone_number)

        @client.on(events.NewMessage(chats=chat_ids))
        async def message_handler(event):
            try:
                log.info("handler start %s %s", event.chat_id, phone_number)
                if event.chat_id in chat_ids and not event.message.out:
                    log.info("handler chats verify ok %s %s", event.chat_id, phone_number)

                    message_text = event.message.text.lower() if event.message.text else ""
                    chat_data = chats.get(event.chat_id)
                    triggers = parse_keywords(chat_data.get("triggers"))
                    log.info("triggers %s", triggers)

                    if all(trigger in message_text for trigger in triggers) or triggers == []:
                        try:
                            result = await process_and_reply.kiq(
                                phone_number=phone_number,
                                chat_id=event.chat_id,
                                message_id=event.message.id,
                                original_text=event.message.text,
                                system_prompt=chat_data.get("system_prompt"),
                            )

                            log.info("Sent to broker: %s", result)
                        except Exception as e:
                            log.error("Broker error: %s", e)
            finally:
                pass
    try:
        # monitor_task = asyncio.create_task(background_memory_monitor())

        client = await tg_manager_for_worker.get_client(phone_number)

        chats_obj = await get_users_channels(user_id)
        chats = {
            chat.chat_id: {
                "system_prompt": chat.system_prompt,
                "triggers": chat.triggers,
            }
            for chat in chats_obj
        }
        chat_ids = list(chats.keys())
        log.info("chat_ids: %s", chat_ids)

        await register_tg_handler()

        await client.run_until_disconnected()

    except Exception as e:
        log.error("Main task error: %s", e)
    finally:
        # ФИНАЛЬНЫЙ ЗАМЕР
        memory_final = process.memory_info().rss / 1024 / 1024
        log.info(f"🏁 FINAL - Memory: {memory_final:.2f} MB")
        monitor_task.cancel()
        await tg_manager_for_worker.close_client(phone_number)

async def reply_to_message(phone_number, chat_id, message_id, reply_text):
    try:
        client = await tg_managers["worker"].get_client(phone_number)
        chat_entity = await client.get_entity(chat_id)
        log.info("Ответ budet отправлен на сообщение %s", message_id)
        await client.send_message(
            entity=chat_entity, message=reply_text, reply_to=message_id
        )
        log.info("Ответ отправлен на сообщение %s", message_id)
    except Exception as e:
        log.error("Ошибка отправки: %s", e, exc_info=True)
    # finally:
    #     await tg_manager_for_task.close()


@broker.task
async def process_and_reply(phone_number, chat_id, message_id, original_text, system_prompt):
    """Обработка и отправка ответа"""
    content = await generate_content(original_text, system_prompt)
    # content = original_text + " test"
    await reply_to_message(phone_number, chat_id, message_id, content)
