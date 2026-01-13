from pyrogram import Client, filters
from database.thumb import get_thumb
from utils.progress import show_progress

PENDING = {}

@Client.on_callback_query(filters.regex("^menu_rename$"))
async def rename_menu(client, query):
    await query.message.reply_text("✏️ Send your file/video now for rename.")
    await query.answer()

@Client.on_message(filters.document | filters.video | filters.audio)
async def file_in(client, message):
    PENDING[message.from_user.id] = message
    await message.reply_text("✏️ Send new file name:")

@Client.on_message(filters.text & ~filters.regex(r"^/"))
async def rename_name(client, message):
    uid = message.from_user.id
    if uid not in PENDING:
        return

    src = PENDING.pop(uid)
    new_name = message.text.strip()

    prog = await message.reply_text("⏳ Renaming...")
    await show_progress(prog, "Renaming...")

    thumb = await get_thumb(uid)
    thumb_id = thumb["file_id"] if thumb else None

    path = await src.download()

    await message.reply_document(
        path,
        file_name=new_name,
        thumb=thumb_id,
        caption="✅ Renamed Successfully!"
    )
    try:
        await prog.delete()
    except:
        pass
