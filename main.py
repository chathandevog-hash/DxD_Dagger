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
app = Flask(__name__)

@app.get("/")
def home():
    return "✅ DxD_Dagger Alive"

@app.get("/health")
def health():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ---------------- BOT ----------------
def create_bot():
    return Client(
        "DxD_Dagger",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workers=20,
        in_memory=True  # 🔥 IMPORTANT FOR RENDER
    )

bot = create_bot()

async def run_bot():
    try:
        await init_db()
        print("✅ MongoDB connected")

        # 🔥 REGISTER HANDLERS FIRST
        load_plugins(bot)
        print("✅ Plugins registered")

        # 🔥 THEN START BOT
        await bot.start()
        print("✅ Bot started")

        await idle()
    except Exception as e:
        print("❌ BOT ERROR:", e)
        traceback.print_exc()
    finally:
        await bot.stop()

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(run_bot())
