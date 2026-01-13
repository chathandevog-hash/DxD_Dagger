from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "DxD_Dagger",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=30
)
