import os
import threading
import asyncio
import traceback
from flask import Flask
from pyrogram import Client, idle

from config import API_ID, API_HASH, BOT_TOKEN
from utils.loader import load_plugins
from database.mongo import init_db

# ---------------- WEB ----------------
app_web = Flask(__name__)

@app_web.get("/")
def home():
    return "✅ DxD_Dagger Alive"

@app_web.get("/health")
def health():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# ---------------- BOT ----------------
bot = Client(
    "DxD_Dagger",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=30
)

async def run_bot():
    try:
        await init_db()
        print("✅ MongoDB connected")

        await bot.start()
        print("✅ Bot connected to Telegram")

        load_plugins()   # ✅ FIXED
        print("✅ Plugins loaded")

        await idle()

    except Exception as e:
        print("❌ BOT ERROR:", e)
        traceback.print_exc()

if __name__ == "__main__":
    t = threading.Thread(target=run_web, daemon=True)
    t.start()

    asyncio.run(run_bot())
