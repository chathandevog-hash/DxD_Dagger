from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_SUB, FORCE_SUB_CHANNEL

async def force_sub_check(client, message):
    if not FORCE_SUB:
        return True

    user_id = message.from_user.id
    try:
        await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return True
    except UserNotParticipant:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@','')}")],
            [InlineKeyboardButton("🔄 Retry", callback_data="forcesub_retry")]
        ])
        await message.reply_text("🔒 Join channel first!", reply_markup=kb)
        return False
    except:
        return True
