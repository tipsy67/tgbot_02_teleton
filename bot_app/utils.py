from openai import OpenAI
from telethon import TelegramClient

from core.config import settings
from core.tg_client import TelegramManager, tg_manager_for_task


async def generate_content(text: str) -> str:

    prompt_system = "Ты Диоген"

    prompt = f"""
    Ты профессиональный пьющий философ. Отвечай на сообщение философски.
    Можно стихами. 
    Вот сообщение:
    {text}
    Верни в ответе текст отформатированный для сообщения телеграм.
    """

    client_ai = OpenAI(api_key=settings.deepseek.api_key, base_url=settings.deepseek.api_url)

    response = client_ai.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )

    new_answer = response.choices[0].message.content
    return new_answer


async def reply_to_message(chat_id, message_id, reply_text):
    """Отправка ответа на конкретное сообщение по ID"""
    try:
        client = await tg_manager_for_task.get_client()
        chat_entity = await client.get_entity(chat_id)

        await client.send_message(
            entity=chat_entity,
            message=reply_text,
            reply_to=message_id
        )
        print(f"✅ Ответ отправлен на сообщение {message_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
    finally:
        await tg_manager_for_task.close()
