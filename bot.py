import asyncio
import logging

from aiogram import Router, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from helpers import build_menu, Registration, MENU
from helpers import save_user, is_registered, main_keyboard, build_cart_keyboard, refresh_cart, Checkout

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

#SETTING UP THE DISPATCHER
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


#START COMMAND THAT REGISTERS USERS
@router.message(Command("start"))
async def start_handler(message: Message, state:FSMContext):
    logger.info(f"User {message.from_user.id} sent: {message.text}")

    #If registered
    if is_registered(message.from_user.id):
        await state.clear()
        await message.answer(
            "👋 Xush kelibsiz!",
            reply_markup=main_keyboard()
        )
        return
    
    #If not registered
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="☎️Raqamingizni Ulashing", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Assalomu alekum.\nKuchli catering botiga xush kelibsiz\nRo'yxatdan o'tish uchun telefon raqamingizni yuboring.",reply_markup=phone_keyboard)
    await state.set_state(Registration.waiting_for_phone)


#PHONE HANDLER
@router.message(Registration.waiting_for_phone, F.contact)
async def phone_handler(message:Message,state:FSMContext):
    contact = message.contact

    #Verify phone number and user id
    if contact.user_id != message.from_user.id:
        await message.answer(
            "❌ Iltimos o'zingizni Raqamingizni jo'nating!",
        )
        return

    phone_number = contact.phone_number

    #Save (for now print)
    save_user(message.from_user.id,phone_number)
    logger.info(f"User {message.from_user.id} sent: {phone_number}")

    #Clear the state
    await state.clear()

    #Change the keyboard
    await message.answer(
        "✅ Ro'yxatdan o'tildi!",
        reply_markup=main_keyboard()
    )


#IF DIDN'T USE THE BUTTON
@router.message(Registration.waiting_for_phone)
async def wrong_input(message: Message):
    await message.answer("Iltimos tugma yordamida raqamingizni ulashing!")

#SHOWS MENU
@router.message(F.text=="📋 Menu")
async def show_menu(message: Message):
    #If not registered
    if not is_registered(message.from_user.id):
        await message.answer("Iltimos avval ro'yxatdan o'ting. /start")
        return
    
    #if registered
    await message.answer(
        "🍽 Bugungi Menu:",
        reply_markup=build_menu()
    )

#ADDS ITEM TO TEMP CART
@router.callback_query(F.data.startswith("add:"))
async def add_to_cart(callbackquery: CallbackQuery, state: FSMContext):
    item_id = int(callbackquery.data.split(":")[1])

    cart = await state.get_data()
    cart_items = cart.get("cart",{})

    #Add item to cart and its number
    cart_items[item_id] = cart_items.get(item_id, 0) + 1
    
    await state.update_data(cart=cart_items)

    item = MENU[item_id]

    await callbackquery.answer(f"{item['name']} savatga qo'shildi.")

#VIEW CART ITEMS
@router.message(F.text=="🛒 Savat")
async def view_cart(message: Message,state: FSMContext):
    
    #Get cart
    data = await state.get_data()
    cart = data.get("cart",{})

    #If cart empty
    if not cart:
        await message.answer("🛒 Savatingiz bo'sh")
        return
    
    #If not empty, show cart
    text = "🛒 Savatingiz:\n\n"
    total = 0

    for item_id,number in cart.items():
        item = MENU[item_id]
        text += f"{number}x {item['name']} - {item['price']} so'm\n"
        total+=item["price"]*number

    text += f"\n💰Jami: {total}so'm"
    
    #Inline keyboards to edit cart
    keyboard = build_cart_keyboard(cart)

    await message.answer(text, reply_markup=keyboard)


#CLEAR CART
@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cart={})

    await callback.message.edit_text(
        "🗑 Savat tozalandi."
    )

    await callback.answer()

#IF + IS PRESSED
@router.callback_query(F.data.startswith("plus:"))
async def plus_item(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split(":")[1])

    data = await state.get_data()
    cart = data.get("cart", {})

    cart[item_id] += 1

    await state.update_data(cart=cart)

    await refresh_cart(callback, state)

    await callback.answer()

#IF - IS PRESSED
@router.callback_query(F.data.startswith("minus:"))
async def minus_item(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split(":")[1])

    data = await state.get_data()
    cart = data.get("cart", {})

    cart[item_id] -= 1

    if cart[item_id] <= 0:
        del cart[item_id]

    await state.update_data(cart=cart)

    await refresh_cart(callback, state)

    await callback.answer()

#CHECKOUT PHASE
@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    cart = data.get("cart", {})

    if not cart:
        await callback.answer("Savat bo'sh")
        return
    
    await callback.message.answer(
        "Ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(
        Checkout.waiting_for_name
    )

    await callback.answer()


#RECIEVE NAME
@router.message(Checkout.waiting_for_name)
async def recieve_name(message: Message, state: FSMContext):

    await state.update_data(
        customer_name=message.text
    )

    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📍 Lokatsiyani yuborish",
                    request_location=True
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Lokatsiyangizni yuboring:",
        reply_markup=location_keyboard
    )

    await state.set_state(
        Checkout.waiting_for_location
    )

@router.message(Checkout.waiting_for_location,F.location)
async def get_location(message:Message,state:FSMContext):

    #Saving the location
    await state.update_data(
        latititude = message.location.latitude,
        longtitude = message.location.longitude
    )

    data = await state.get_data()   

    #Confirming the order
    confirm_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data="confirm_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_order"
                )
            ]
        ]
    )

    await message.answer(
    f"""
    Buyurtma tayyor:

    👤 {data['customer_name']}

    📍 Lokatsiya qabul qilindi

    Buyurtmani tasdiqlaysizmi?.
    """,
    reply_markup=confirm_keyboard
    )

