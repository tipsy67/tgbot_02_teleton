import logging

from bot_app.utils import generate_content
from core.taskiq_broker import broker
from core.tg_client import tg_managers

log = logging.getLogger(__name__)


async def reply_to_message(phone_number, chat_id, message_id, reply_text):
    try:
        client = await tg_managers["worker"].get_client(phone_number)
        chat_entity = await client.get_entity(chat_id)

        await client.send_message(
            entity=chat_entity, message=reply_text, reply_to=message_id
        )
        log.info("Ответ отправлен на сообщение %s", message_id)
    except Exception as e:
        log.error("Ошибка отправки: %s", e, exc_info=True)
    # finally:
    #     await tg_manager_for_task.close()


@broker.task
async def process_and_reply(phone_number, chat_id, message_id, original_text):
    """Обработка и отправка ответа"""
    content = await generate_content(original_text)
    # content = original_text + " test"
    await reply_to_message(phone_number, chat_id, message_id, content)
