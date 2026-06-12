from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State

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

