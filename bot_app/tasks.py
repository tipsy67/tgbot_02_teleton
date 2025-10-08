from bot_app.utils import generate_content, reply_to_message
from core.taskiq_broker import broker


@broker.task
async def process_and_reply(chat_id, message_id, original_text):
    """Обработка и отправка ответа"""
    content = await generate_content(original_text)
    await reply_to_message(chat_id, message_id, content)

