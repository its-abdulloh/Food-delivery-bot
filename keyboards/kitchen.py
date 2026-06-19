from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kitchen_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Orders")],
        [KeyboardButton(text="📊 Summary")]
    ],
    resize_keyboard=True
)