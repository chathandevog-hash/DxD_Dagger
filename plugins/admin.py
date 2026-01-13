from pyrogram import Client, filters
from utils.helpers import is_admin
from database.mongo import db

@Client.on_message(filters.command("stats"))
async def stats(client, message):
    if not is_admin(message.from_user.id):
        return

    total_users = await db["users"].count_documents({})
    thumbs = await db["thumbs"].count_documents({})

    await message.reply_text(
        f"📊 Admin Stats\n\n"
        f"👥 Users: {total_users}\n"
        f"🖼 Thumbnails: {thumbs}\n"
    )
