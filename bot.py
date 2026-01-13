import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from utils.loader import load_plugins
from database.mongo import init_db

app = Client(
    "RenameProBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

async def main():
    await init_db()
    await app.start()
    load_plugins()
    print("✅ RenameProBot Started")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
