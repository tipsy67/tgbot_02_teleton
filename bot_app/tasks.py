import asyncio
import logging

from taskiq import Context, TaskiqDepends
from telethon import events

from bot_app.utils import generate_content
from core.db_helper import db_helper
from core.redis_store import HealthCheckManager, CancelCheckManager
from core.taskiq_broker import broker
from core.tg_client import tg_managers
from data_app.crud.channel import get_users_channels



log = logging.getLogger(__name__)
tg_manager_for_worker = tg_managers["worker"]


def parse_keywords(text: str, delimiter: str = ",") -> list[str]:
    """Парсит строку с ключевыми словами в список"""
    if not text:
        return []

    return [word.strip() for word in text.split(delimiter) if word.strip()]


@broker.task
async def initial_client(user_id: int, phone_number: str, context:Context=TaskiqDepends()):

    async def background_timestamp(task_id_lcl: str):
        """Фоновая задача для мониторинга"""
        log.info("Start healthcheck fo %s", task_id_lcl)
        try:
            while True:
                await HealthCheckManager.set_timestamp(task_id_lcl)
                await asyncio.sleep(120)
        except asyncio.CancelledError:
            log.info("Background timestamp task %s cancelled", task_id)
        finally:
            pass

    async def register_tg_handler():
        log.info("Register handler %s %s", user_id, phone_number)

        @client.on(events.NewMessage(chats=chat_ids))
        async def message_handler(event):
            try:
                log.info("Handler start %s %s", event.chat_id, phone_number)
                if event.chat_id in chat_ids and not event.message.out:
                    log.info("Handler chats verify ok %s %s", event.chat_id, phone_number)

                    message_text = event.message.text.lower() if event.message.text else ""
                    chat_data = chats.get(event.chat_id)
                    triggers = parse_keywords(chat_data.get("triggers"))
                    log.info("Triggers %s", triggers)

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

    task_id = str(context.message.task_id)
    monitor_task = asyncio.create_task(background_timestamp(task_id))
    try:
        client = await tg_manager_for_worker.get_client(phone_number)

        async with db_helper.session_factory() as session:
            chats_obj = await get_users_channels(user_id, session)

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

        client_loop_obj = asyncio.create_task(client.run_until_disconnected())
        while not client_loop_obj.done():
            await asyncio.sleep(30)
            if await CancelCheckManager.get(task_id)=="1":
                log.info("Cancel requested for task %s", task_id)
                client_loop_obj.cancel()

                try:
                    await asyncio.wait_for(client_loop_obj, timeout=10.0)
                    log.info("Telethon client stopped gracefully for task %s", task_id)
                except asyncio.TimeoutError:
                    log.warning("Telethon client task didn't stop in time for task %s", task_id)
                except asyncio.CancelledError:
                    log.info("Telethon client task was cancelled successfully for task %s",
                             task_id)
                break

        log.info("Client processing completed for task %s", task_id)

    except Exception as e:
        log.error("Main task error: %s", e)
    finally:
        await HealthCheckManager.delete(task_id)
        await CancelCheckManager.delete(task_id)
        if monitor_task and not monitor_task.done():
            monitor_task.cancel()
            try:
                await asyncio.wait_for(monitor_task, timeout=5)
            except asyncio.TimeoutError:
                log.warning("Monitor task %s didn't cancel in time", task_id)

        await tg_manager_for_worker.close_client(phone_number)


async def reply_to_message(phone_number, chat_id, message_id, reply_text):
    try:
        client = await tg_managers["worker"].get_client(phone_number)
        chat_entity = await client.get_entity(chat_id)
        log.info("Prepare send reply on message: %s", message_id)
        await client.send_message(
            entity=chat_entity, message=reply_text, reply_to=message_id
        )
        log.info("Reply send on message: %s", message_id)
    except Exception as e:
        log.error("Error on send: %s", e, exc_info=True)
    # finally:
    #     await tg_manager_for_task.close()


@broker.task
async def process_and_reply(phone_number, chat_id, message_id, original_text, system_prompt):
    """Обработка и отправка ответа"""
    content = await generate_content(original_text, system_prompt)
    # content = original_text + " test"
    await reply_to_message(phone_number, chat_id, message_id, content)
