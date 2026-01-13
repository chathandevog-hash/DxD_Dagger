from pyrogram import Client, filters
from config import BATCH_LIMIT
from database.thumb import get_thumb
from utils.progress import show_progress

MODE = {}
FILES = {}

@Client.on_message(filters.command("batches"))
async def batches(client, message):
    uid = message.from_user.id
    MODE[uid] = True
    FILES[uid] = []
    await message.reply_text(
        f"✅ Batch Rename ON\n"
        f"📌 Send upto {BATCH_LIMIT} files.\n"
        f"Type /done when finished."
    )

@Client.on_message(filters.command("done"))
async def done(client, message):
    uid = message.from_user.id
    if uid not in MODE:
        return await message.reply_text("❌ Use /batches first.")
    if len(FILES.get(uid, [])) == 0:
        return await message.reply_text("❌ No files received.")
    MODE[uid] = "WAITNAME"
    await message.reply_text("✏️ Send common rename name:")

@Client.on_message(filters.document | filters.video | filters.audio)
async def collect(client, message):
    uid = message.from_user.id
    if uid not in MODE:
        return

    if MODE[uid] is True:
        if len(FILES[uid]) >= BATCH_LIMIT:
            return await message.reply_text(f"⚠️ Limit reached {BATCH_LIMIT}. Type /done.")
        FILES[uid].append(message)
        await message.reply_text(f"✅ Added ({len(FILES[uid])}/{BATCH_LIMIT})")

@Client.on_message(filters.text & ~filters.regex(r"^/"))
async def batch_process(client, message):
    uid = message.from_user.id
    if uid not in MODE:
        return
    if MODE[uid] != "WAITNAME":
        return

    common = message.text.strip()
    msgs = FILES[uid]

    prog = await message.reply_text("⏳ Batch Renaming...")
    await show_progress(prog, "Batch Renaming...")

    thumb = await get_thumb(uid)
    thumb_id = thumb["file_id"] if thumb else None

    for i, m in enumerate(msgs, start=1):
        p = await m.download()
        out = f"{common}_{i}"
        await message.reply_document(
            p,
            file_name=out,
            thumb=thumb_id,
            caption=f"✅ Batch {i}/{len(msgs)}"
        )

    MODE.pop(uid, None)
    FILES.pop(uid, None)
    try:
        await prog.delete()
    except:
        pass
