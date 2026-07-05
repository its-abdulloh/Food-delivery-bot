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
        keyboard=[
            [
                InlineKeyboardButton("➕",callback_data="increase"),
                InlineKeyboardButton(f"{item_amount}"),
                InlineKeyboardButton("➖",callback_data="decrease"),
                InlineKeyboardButton("🛒 Savatga qo'shish",callback_data=f"add:{item_id}")
            ]
        ]
    )