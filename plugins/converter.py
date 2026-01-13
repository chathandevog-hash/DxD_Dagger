from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.progress import show_progress

STATE = {}

def convert_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎞 Video ➜ File", callback_data="cv_v2f"),
            InlineKeyboardButton("📁 File ➜ Video", callback_data="cv_f2v"),
        ]
    ])

@Client.on_callback_query(filters.regex("^menu_convert$"))
async def convert_menu(client, query):
    await query.message.reply_text("🎞 Send file/video, then choose 👇", reply_markup=convert_kb())
    await query.answer()

@Client.on_message(filters.video | filters.document)
async def catch_media(client, message):
    STATE[message.from_user.id] = {"msg": message}
    await message.reply_text("Choose convert option 👇", reply_markup=convert_kb())

@Client.on_callback_query(filters.regex("^cv_(v2f|f2v)$"))
async def cv_choose(client, query):
    uid = query.from_user.id
    if uid not in STATE:
        return await query.answer("Send file/video first", show_alert=True)
    STATE[uid]["mode"] = query.data.split("_")[1]
    await query.message.reply_text("✏️ Send rename name:")
    await query.answer()

@Client.on_message(filters.text & ~filters.command)
async def cv_rename(client, message):
    uid = message.from_user.id
    if uid not in STATE:
        return
    st = STATE[uid]
    if "mode" not in st:
        return

    rename = message.text.strip()
    msg = st["msg"]
    mode = st["mode"]

    prog = await message.reply_text("⏳ Converting...")
    await show_progress(prog, "Converting...")

    p = await msg.download()

    if mode == "v2f":
        await message.reply_document(p, file_name=f"{rename}.mp4", caption="✅ Converted")
    else:
        await message.reply_video(p, caption=f"✅ Converted: {rename}")

    STATE.pop(uid, None)
    try:
        await prog.delete()
    except:
        pass
