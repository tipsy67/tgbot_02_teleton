from dotenv import load_dotenv
from telethon import TelegramClient
import os

from bot_app.taskiq_broker import broker

# Remember to use your own values from my.telegram.org!
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
client = TelegramClient('anon', int(api_id), api_hash)

async def example():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    # You can send messages to yourself...
    await client.send_message('me', 'Hello, myself!')
    # ...to some chat ID
    await client.send_message(-4921301938, 'Hello, group!')
    # ...to your contacts
    await client.send_message('+79107253745', 'Hello, friend!')
    # ...or even to any username
    await client.send_message('dantoropov', 'Testing Telethon!')

    # You can, of course, use markdown in your messages:
    message = await client.send_message(
        'me',
        'This message has **bold**, `code`, __italics__ and '
        'a [nice website](https://example.com)!',
        link_preview=False
    )

    # Sending a message returns the sent message object, which you can use
    print(message.raw_text)

    # You can reply to messages directly if you have a message object
    await message.reply('Cool!')

    # Or send files, songs, documents, albums...
    await client.send_file('me', './static/images/IMG-20250623-WA0007.jpg')

    # You can print the message history of any chat:
    async for message in client.iter_messages('me'):
        print(message.id, message.text)

        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)  # printed after download is done

async def main():
    await broker.startup()
    await broker.shutdown()

with client:
    client.loop.run_until_complete(main())