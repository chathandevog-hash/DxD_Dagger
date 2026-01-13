import os
import logging
from pyrogram import Client, filters
from flask import Flask

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------- Config ----------
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

if API_ID == 0 or not API_HASH or not BOT_TOKEN:
    raise SystemExit("❌ API_ID / API_HASH / BOT_TOKEN env var set ചെയ്തിട്ടില്ല!")

# ---------- Flask Web (Render keep-alive) ----------
app_web = Flask(__name__)

@app_web.get("/")
def home():
    return "✅ Bot is running!"

# ---------- Bot ----------
app = Client(
    "DxD_Dagger",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "✅ Bot started!\n\nCommands:\n/start\n/ping"
    )

@app.on_message(filters.command("ping"))
async def ping_cmd(client, message):
    await message.reply_text("🏓 Pong!")

if __name__ == "__main__":
    logging.info("✅ Starting bot...")
    app.run()
