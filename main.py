import os
import threading
import asyncio
import traceback
from flask import Flask
from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN
from utils.loader import load_plugins
from database.mongo import init_db

# ---------------- FLASK ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ DxD_Dagger Alive"

@app.route("/health")
def health():
    return "OK"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ---------------- BOT ----------------
bot = Client(
    "DxD_Dagger",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=10,
    in_memory=True
)

async def bot_runner():
    try:
        await init_db()
        print("✅ MongoDB connected")

        load_plugins(bot)
        print("✅ Plugins registered")

        await bot.start()
        print("✅ Bot connected to Telegram")

        # 🔥 DO NOT USE idle() ON RENDER
        await asyncio.Event().wait()

    except Exception as e:
        print("❌ BOT ERROR:", e)
        traceback.print_exc()
    finally:
        await bot.stop()

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot_runner())

# ---------------- MAIN ----------------
if __name__ == "__main__":
    # Start bot in background thread
    threading.Thread(target=start_bot, daemon=True).start()

    # Start Flask (Render expects this)
    run_flask()
