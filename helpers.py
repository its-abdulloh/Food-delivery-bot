from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime


import sqlite3
import json

#USER ROLES
USERS = {
    123456789: "admin",
    987654321: "kitchen",
    555555555: "driver",
}

#TEMPORARY MENU
MENU = {
    1: {"name": "Burger", "price": 10000},
    2: {"name": "Pizza", "price": 12000},
    3: {"name": "Salad", "price": 7000},
}

#IDs
ADMIN_ID = 34324043
KITCHEN_ID = 987654321
DRIVERS = {
    111111111: "Ali",
    222222222: "Bek",
    333333333: "John",
}
def is_admin(user_id):
    return user_id == ADMIN_ID


def is_kitchen(user_id):
    return user_id == KITCHEN_ID


def is_driver(user_id):
    return user_id in DRIVERS

#DETERMINE THE USER ROLE
def get_role(user_id: int) -> str:
    return USERS.get(user_id, "customer")

#GET LOCATION
def build_map_link(latitude,longitude):
    return f"https://maps.google.com/?q={latitude},{longitude}"

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

def is_registered(user_id: int) -> bool:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE telegram_id=?",
        (user_id,)
    )

    result = cursor.fetchone() is not None

    conn.close()

    return result

def save_user(user_id: int, phone: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (telegram_id, phone) VALUES (?, ?)",
        (user_id, phone)
    )
    conn.commit()
    conn.close()

def get_phone(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    phone = cursor.execute("SELECT phone FROM users WHERE telegram_id=?",(user_id,)).fetchone()[0]
    return phone

def create_order(data:dict,user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # calculate total from cart
    cart = data.get("cart", {})
    total=0

    for item_id, qty in cart.items():
        item = MENU[int(item_id)]
        total += item["price"] * qty

    phone = get_phone(user_id)

    cursor.execute("""
        INSERT INTO orders (
            user_id,
            customer_name,
            phone,
            items,
            total,
            latitude,
            longitude,
            status,
            payment_file_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        data.get("customer_name"),
        phone,
        json.dumps(cart),          # items TEXT
        total,
        data.get("latitude"),
        data.get("longitude"),
        "PENDING",
        data.get("payment_file")    
    ))

    conn.commit()

    order_id = cursor.lastrowid
    conn.close()

    return order_id

def update_order_status(order_id: int, status: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET status=? WHERE id=?",
        (status, order_id)
    )

    conn.commit()
    conn.close()

def update_status_where(prev:str, new:str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET status=? WHERE status=?",
        (new, prev)
    )

    conn.commit()
    conn.close()

def get_order(order_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            customer_name,
            phone,
            items,
            total,
            latitude,
            longitude
        FROM orders
        WHERE id=?
    """, (order_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "user_id": row[0],
        "customer_name": row[1],
        "phone": row[2],
        "items": json.loads(row[3]),
        "total": row[4],
        "latitude": row[5],
        "longitude": row[6]
    }

def get_order_user(order_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM orders WHERE id=?",
        (order_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None
      

# def generate_kitchen_summary():
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT items
#         FROM orders
#         WHERE status = 'CONFIRMED'
#     """)

#     rows = cursor.fetchall()
#     conn.close()

#     summary = {}

#     for (items_json,) in rows:
#         items = json.loads(items_json)

#         for item_id, qty in items.items():
#             item_id = int(item_id)

#             if item_id not in summary:
#                 summary[item_id] = 0

#             summary[item_id] += qty

#     return summary

#SET ORDERS STATUS
def set_orders_open(is_open: bool):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE settings
        SET value = ?
        WHERE key = 'orders_open'
        """,
        ("1" if is_open else "0",)
    )

    conn.commit()
    conn.close()

#CHECK IF ITS OPEN
def orders_are_open():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT value
        FROM settings
        WHERE key = 'orders_open'
        """
    )

    row = cursor.fetchone()

    conn.close()

    return row and row[0] == "1"

#MENU
def add_menu_item(name, price):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO menu (name, price) VALUES (?, ?)",
        (name, price)
    )

    conn.commit()
    conn.close()

def clear_menu():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM menu"
    )

    conn.commit()
    conn.close()


def get_menu():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, price FROM menu")

    rows = cursor.fetchall()
    conn.close()

    return rows


def seed_menu_from_dict():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # optional: clear existing menu
    cursor.execute("DELETE FROM menu")

    for item_id, item in MENU.items():
        cursor.execute(
            "INSERT INTO menu (name, price) VALUES (?, ?)",
            (item["name"], item["price"])
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_menu_from_dict()