from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Buyurtmalar")],
        [KeyboardButton(text="🍔 Menu")],
    ],
    resize_keyboard=True
)