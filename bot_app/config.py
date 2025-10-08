import os

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
DEEPSEEK_API_URL = os.environ.get("DEEPSEEK_API_URL")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

client = TelegramClient('anon', int(API_ID), API_HASH)