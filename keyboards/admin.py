from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_keyboard(orders_open: bool):
    if orders_open:
        toggle_btn = KeyboardButton(text="🔴 Buyurtmalarni to'xtatish")
    else:
        toggle_btn = KeyboardButton(text="🟢 Buyurtmalarni boshlash")

    return ReplyKeyboardMarkup(
        keyboard=[
            [toggle_btn],
            [KeyboardButton(text="📋 Bugungi Menu")]
            # [KeyboardButton(text="👨‍🍳 Oshxonaga jo'natish")]
        ],
        resize_keyboard=True
    )

def admin_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="➕ Qo'shish")
    builder.button(text="🗑 O'chirish")
    builder.button(text="🧹 Tozalash")

    builder.button(text="📋 Menu")
    builder.button(text="🔙 Orqaga")

    builder.adjust(2, 2, 1)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
