from bot_app.taskiq_broker import broker


@broker.task
def remake_article(text: str):
    generate_content(product_id)

