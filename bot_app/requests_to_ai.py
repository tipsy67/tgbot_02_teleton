import os

from openai import OpenAI


def generate_content(product_id: int) -> None:
    DEEPSEEK_API_URL = "https://api.deepseek.com/"
    API_KEY = os.environ.get("DEEPSEEK_API_KEY")


    prompt = f"""
    Ты профессиональный верстальщик HTML. Преобразуй текст статьи блога в HTML-блоки, 
    которые будут соответствовать стилям и структуре указанного шаблона. 
    Стиль изложения и содержимое оставь без изменений.


    Верни в ответе чистый HTML без всяких примечаний.
    """

    client = OpenAI(api_key=API_KEY, base_url=DEEPSEEK_API_URL)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Ты профессиональный верстальщик HTML."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )

    new_article = response.choices[0].message.content


