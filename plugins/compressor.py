import os, subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.progress import show_progress

STATE = {}

def q_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 1080p", callback_data="q_1080"), InlineKeyboardButton("🎞 720p", callback_data="q_720")],
        [InlineKeyboardButton("📺 480p", callback_data="q_480"), InlineKeyboardButton("📱 360p", callback_data="q_360")],
        [InlineKeyboardButton("🔻 240p", callback_data="q_240"), InlineKeyboardButton("📷 144p", callback_data="q_144")],
    ])

@Client.on_callback_query(filters.regex("^menu_compress$"))
async def comp_menu(client, query):
    await query.message.reply_text("🗜 Send video to compress.")
    await query.answer()

@Client.on_message(filters.video)
async def catch_video(client, message):
    STATE[message.from_user.id] = {"msg": message}
    await message.reply_text("Select quality 👇", reply_markup=q_kb())

@Client.on_callback_query(filters.regex("^q_(1080|720|480|360|240|144)$"))
async def q_choose(client, query):
    uid = query.from_user.id
    if uid not in STATE:
        return await query.answer("Send video first", show_alert=True)
    STATE[uid]["q"] = int(query.data.split("_")[1])
    await query.message.reply_text("✏️ Send rename name:")
    await query.answer()

@Client.on_message(filters.text & ~filters.regex(r"^/"))
async def comp_run(client, message):
    uid = message.from_user.id
    if uid not in STATE:
        return
    st = STATE[uid]
    if "q" not in st:
        return

    rename = message.text.strip()
    q = st["q"]
    src = st["msg"]

    prog = await message.reply_text("⏳ Compressing...")
    await show_progress(prog, f"Compressing {q}p...")

    in_path = await src.download()
    os.makedirs("output", exist_ok=True)
    out_path = f"output/{uid}_{q}.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-i", in_path,
        "-vf", f"scale=-2:{q}",
        "-preset", "veryfast",
        "-crf", "28",
        out_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        await message.reply_video(out_path, caption=f"✅ Compressed {q}p\nName: {rename}")
    except:
        await message.reply_text("❌ ffmpeg not found / compression failed.")

    STATE.pop(uid, None)
    try:
        await prog.delete()
    except:
        pass
