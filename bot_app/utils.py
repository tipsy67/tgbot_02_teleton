import os

from openai import OpenAI
from telethon import TelegramClient

from bot_app.config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, client, API_ID, API_HASH


async def generate_content(text: str) -> str:

    promt_system = "Ты Диоген"

    prompt = f"""
    Ты профессиональный пьющий философ. Отвечай на сообщение философски.
    Можно стихами. 
    Вот сообщение:
    {text}
    Верни в ответе текст отформатированный для сообщения телеграм.
    """

    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": promt_system},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )

    new_answer = response.choices[0].message.content
    return new_answer


async def reply_to_message(chat_id, message_id, reply_text):
    """Отправка ответа на конкретное сообщение по ID"""
    async with TelegramClient('anon', int(API_ID), API_HASH) as client:
        try:
            chat_entity = await client.get_entity(chat_id)

            await client.send_message(
                entity=chat_entity,
                message=reply_text,
                reply_to=message_id
            )
            print(f"✅ Ответ отправлен на сообщение {message_id}")
        except Exception as e:
            print(f"❌ Ошибка отправки: {e}")

