from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_keyboard(orders_open: bool):
    if orders_open:
        toggle_btn = KeyboardButton(text="🔴 Buyurtmalarni to'xtatish")
    else:
        toggle_btn = KeyboardButton(text="🟢 Buyurtmalarni boshlash")

    return ReplyKeyboardMarkup(
        keyboard=[
            [toggle_btn],
            # [KeyboardButton(text="👨‍🍳 Oshxonaga jo'natish")]
        ],
        resize_keyboard=True
    )