import os
import threading
import asyncio
from flask import Flask
from pyrogram import Client, idle

from config import API_ID, API_HASH, BOT_TOKEN
from utils.loader import load_plugins
from database.mongo import init_db

# -------------------- WEB (Health) --------------------
app_web = Flask(__name__)

@app_web.get("/")
def home():
    return "✅ RenameProBot Web Alive"

@app_web.get("/health")
def health():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# -------------------- BOT --------------------
bot = Client(
    "RenameProBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

async def run_bot():
    await init_db()
    await bot.start()
    load_plugins()
    print("✅ RenameProBot Started")
    await idle()
    await bot.stop()

if __name__ == "__main__":
    # Start web in separate thread
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

    # Start bot
    asyncio.run(run_bot())
