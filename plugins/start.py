from pyrogram import filters
from bot_instance import bot

from utils.buttons import main_menu
from plugins.force_sub import force_sub_check
from database.users import add_user

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    ok = await force_sub_check(client, message)
    if not ok:
        return

    await add_user(message.from_user.id)

    await message.reply_text(
        "👋 Hi!\nSend any file/video.\n\nChoose option 👇",
        reply_markup=main_menu()
    )
