from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

driver_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚚 Meni buyurtmalarim")]
    ],
    resize_keyboard=True
)

