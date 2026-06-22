from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kitchen_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Buyurtmalar")]
    ],
    resize_keyboard=True
)