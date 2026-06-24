from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_keyboard(orders_open: bool):
    if orders_open:
        toggle_btn = KeyboardButton(text="🔴 Buyurtmalarni to'xtatish")
    else:
        toggle_btn = KeyboardButton(text="🟢 Buyurtmalarni boshlash")

    return ReplyKeyboardMarkup(
        keyboard=[
            [toggle_btn],
            [KeyboardButton(text="📋 MENU")]
            # [KeyboardButton(text="👨‍🍳 Oshxonaga jo'natish")]
        ],
        resize_keyboard=True
    )

def get_menu_admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Qo'shsih")],
            [KeyboardButton(text="📋 Menuni ko'rish")],
            [KeyboardButton(text="❌ O'chirish")],
            [KeyboardButton(text="⬅ Orqaga")]
        ],
        resize_keyboard=True
    )