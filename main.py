import os
import threading
import asyncio
import traceback
from flask import Flask
from pyrogram import idle

from utils.loader import load_plugins
from database.mongo import init_db
from bot_instance import bot   # ✅ IMPORT SAME BOT INSTANCE

# -------------------- WEB --------------------
app_web = Flask(__name__)

@app_web.get("/")
def home():
    return "✅ DxD_Dagger Alive"

@app_web.get("/health")
def health():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    print("✅ Web running on port:", port)
    app_web.run(host="0.0.0.0", port=port)

# -------------------- BOT --------------------
async def run_bot():
    try:
        await init_db()
        print("✅ MongoDB connected")

        await bot.start()
        print("✅ Bot connected to Telegram")

        load_plugins()
        print("✅ Plugins loaded")

        await idle()  # keep bot alive

    except Exception as e:
        print("❌ BOT ERROR:", e)
        traceback.print_exc()

if __name__ == "__main__":
    # Start Web Server
    t = threading.Thread(target=run_web, daemon=True)
    t.start()

    # Start Bot
    asyncio.run(run_bot())
