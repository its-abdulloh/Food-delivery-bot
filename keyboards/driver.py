from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

driver_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚚 Meni buyurtmalarim")]
    ],
    resize_keyboard=True
)