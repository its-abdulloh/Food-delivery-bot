from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Orders")],
        [KeyboardButton(text="🍔 Menu")],
        [KeyboardButton(text="🚚 Drivers")],
        [KeyboardButton(text="📊 Summary")],
    ],
    resize_keyboard=True
)