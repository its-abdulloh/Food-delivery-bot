from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

driver_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚚 My Deliveries")]
    ],
    resize_keyboard=True
)