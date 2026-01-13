from pyrogram import Client, filters

@Client.on_message(filters.command("health"))
async def health(client, message):
    await message.reply_text("✅ Alive")
