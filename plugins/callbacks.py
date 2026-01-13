from pyrogram import Client

@Client.on_callback_query()
async def cb_all(client, query):
    if query.data == "forcesub_retry":
        await query.message.edit_text("✅ Now send /start again.")
        await query.answer()
        return
    await query.answer()
