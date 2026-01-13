from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✏️ Rename", callback_data="menu_rename"),
            InlineKeyboardButton("🗜 Compressor", callback_data="menu_compress"),
        ],
        [
            InlineKeyboardButton("🔗 URL Uploader", callback_data="menu_url"),
            InlineKeyboardButton("🎞 Video ↔ File", callback_data="menu_convert"),
        ],
    ])
