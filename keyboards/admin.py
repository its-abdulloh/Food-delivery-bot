from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_keyboard(orders_open: bool):
    if orders_open:
        toggle_btn = KeyboardButton(text="🔴 Close Orders")
    else:
        toggle_btn = KeyboardButton(text="🟢 Open Orders")

    return ReplyKeyboardMarkup(
        keyboard=[
            [toggle_btn],
            [KeyboardButton(text="📋 Buyurtmalar")],
            [KeyboardButton(text="🍔 Menu")],
        ],
        resize_keyboard=True
    )