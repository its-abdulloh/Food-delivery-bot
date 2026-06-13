from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext


import sqlite3


#NEEDED TO WAIT FOR PHONE NUMBER
class Registration(StatesGroup):
    waiting_for_phone = State()

#TEMPORARY MENU
MENU = {
    1: {"name": "Burger", "price": 10000},
    2: {"name": "Pizza", "price": 12000},
    3: {"name": "Salad", "price": 7000},
}

#FUNCTION THAT BUILDS MENU BUTTONS
def build_menu():
    builder = InlineKeyboardBuilder()

    for item_id, item in MENU.items():
        builder.button(
            text=f"{item["name"]} - {item["price"]}sum",
            callback_data=f"add:{item_id}"
        )
    
    builder.adjust(1)
    return builder.as_markup()

#KEYBOARD THAT SHOWS AFTER REGISTRATION
def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📋 Menu"),
                KeyboardButton(text="🛒 Savat")
            ]
        ],
        resize_keyboard=True
    )

#BUILD CART KEYBOARD
def build_cart_keyboard(cart):
    rows = []

    for item_id, quantity in cart.items():
        rows.append([
            InlineKeyboardButton(
                text="➖",
                callback_data=f"minus:{item_id}"
            ),
            InlineKeyboardButton(
                text=str(quantity),
                callback_data="noop"
            ),
            InlineKeyboardButton(
                text="➕",
                callback_data=f"plus:{item_id}"
            )
        ])

    rows.append([
        InlineKeyboardButton(
            text="🗑 Tozalash",
            callback_data="clear_cart"
        )
    ])

    rows.append([
        InlineKeyboardButton(
            text="✅ Buyurtma berish",
            callback_data="checkout"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)

#REFRESH CART AFTER IT'S BEEN EDITED
async def refresh_cart(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", {})

    if not cart:
        await callback.message.edit_text(
            "🛒 Savatingiz bo'sh."
        )
        return

    text = "🛒 Savatingiz:\n\n"
    total = 0

    for item_id, quantity in cart.items():
        item = MENU[item_id]

        text += (
            f"{item['name']} x{quantity}\n"
        )

        total += item["price"] * quantity

    text += f"\n💰 Jami: {total:,} so'm"

    # build keyboard here again
    keyboard = build_cart_keyboard(cart)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )
    

#---------------------------------------SQLITE HELPER FUNCTIONS---------------------------------------
conn = sqlite3.connect("database.db")
cursor = conn.cursor()


def is_registered(user_id: int) -> bool:
    cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (user_id,))
    return cursor.fetchone() is not None


def save_user(user_id: int, phone: str):
    cursor.execute(
        "INSERT INTO users (telegram_id, phone) VALUES (?, ?)",
        (user_id, phone)
    )
    conn.commit()

