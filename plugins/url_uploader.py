import re, os, aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.progress import show_progress

URL_STATE = {}

def url_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 Video", callback_data="url_video"),
            InlineKeyboardButton("📁 File", callback_data="url_file")
        ]
    ])

@Client.on_callback_query(filters.regex("^menu_url$"))
async def url_menu(client, query):
    await query.message.reply_text("🔗 Send URL:")
    await query.answer()

@Client.on_message(filters.text & ~filters.regex(r"^/"))
async def url_message(client, message):
    txt = message.text.strip()
    if not re.match(r"^https?://", txt):
        return
    URL_STATE[message.from_user.id] = {"url": txt}
    await message.reply_text("✅ URL detected. Choose output 👇", reply_markup=url_kb())

@Client.on_callback_query(filters.regex("^url_(video|file)$"))
async def url_out(client, query):
    uid = query.from_user.id
    if uid not in URL_STATE:
        return await query.answer("Send URL first", show_alert=True)
    URL_STATE[uid]["mode"] = query.data.split("_")[1]
    await query.message.reply_text("✏️ Send rename name:")
    await query.answer()

@Client.on_message(filters.text & ~filters.regex(r"^/"))
async def url_rename(client, message):
    uid = message.from_user.id
    if uid not in URL_STATE:
        return
    st = URL_STATE[uid]
    if "mode" not in st:
        return

    rename = message.text.strip()
    url = st["url"]
    mode = st["mode"]

    prog = await message.reply_text("⏳ Downloading...")
    await show_progress(prog, "Downloading URL...")

    os.makedirs("downloads", exist_ok=True)
    out_path = f"downloads/{uid}.bin"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                URL_STATE.pop(uid, None)
                return await message.reply_text("❌ Failed to download.")
            with open(out_path, "wb") as f:
                f.write(await resp.read())

    if mode == "video":
        await message.reply_video(out_path, caption=f"✅ Done: {rename}")
    else:
        await message.reply_document(out_path, file_name=rename, caption="✅ Done")

    URL_STATE.pop(uid, None)
    try:
        await prog.delete()
    except:
        pass
