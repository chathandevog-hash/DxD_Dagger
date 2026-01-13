from pyrogram import Client, filters
from database.thumb import set_thumb, get_thumb, delete_thumb

@Client.on_message(filters.photo)
async def save_thumb(client, message):
    await set_thumb(message.from_user.id, message.photo.file_id)
    await message.reply_text(
        "✅ Thumbnail Saved!\n"
        "📌 Used only for: ✏️ Rename + 🔁 /batches\n\n"
        "Commands:\n"
        "/viewtub - view thumbnail\n"
        "/deletetub - delete thumbnail"
    )

@Client.on_message(filters.command("viewtub"))
async def view_thumb(client, message):
    data = await get_thumb(message.from_user.id)
    if not data:
        return await message.reply_text("❌ No thumbnail set.")
    await message.reply_photo(data["file_id"], caption="✅ Your Current Thumbnail")

@Client.on_message(filters.command("deletetub"))
async def del_thumb(client, message):
    await delete_thumb(message.from_user.id)
    await message.reply_text("✅ Thumbnail deleted successfully ✅")
