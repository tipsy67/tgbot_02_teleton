from openai import OpenAI

from core.config import settings

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



