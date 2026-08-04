from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Menu"),
            KeyboardButton(text="🛒 Savat")
        ]
    ],
    resize_keyboard=True
)

phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="☎️ Raqamingizni Ulashing",
                request_contact=True
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

def menu_item_keyboard(item_id,item_amount:int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text = "➕",callback_data="increase"),
                InlineKeyboardButton(text = f"{item_amount}",callback_data="ignore"),
                InlineKeyboardButton(text = "➖",callback_data="decrease"),
            ],
            [InlineKeyboardButton(text = "🛒 Savatga qo'shish",callback_data=f"add:{item_id}")]
        ]
    )
    return keyboard


item_navigation_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Orqaga"),
            KeyboardButton(text="🛒 Savat")
        ]
    ],
    resize_keyboard=True
)