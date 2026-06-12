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
from helpers import save_user, is_registered

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

#SETTING UP THE DISPATCHER
dp = Dispatcher(storage=MemoryStorage)
router = Router()
dp.include_router(router)


#START COMMAND THAT REGISTERS USERS
@router.message(Command("start"))
async def start_handler(message: Message, state:FSMContext):
    logger.info(f"User {message.from_user.id} sent: {message.text}")

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

    #Clear the keyboard
    await message.answer(
        "✅ Registration successful!",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()


#IF DIDN'T USE THE BUTTON
@router.message(Registration.waiting_for_phone)
async def wrong_input(message: Message):
    await message.answer("Iltimos tugma yordamida raqamingizni ulashing!")


@router.callback_query(lambda c:c.data=="menu")
async def show_menu(message: Message):
    await message.answer(
        "🍽 Bugungi Menu:",
        reply_markup=build_menu()
    )

@router.callback_query(F.data.startswith("add:"))
async def add_to_cart(callbackquery: CallbackQuery, state: FSMContext):
    item_id = int(callbackquery.data.split(":")[1])

    cart = await state.get_data()
    cart_items = cart.get("cart",[])

    cart_items.append(item_id)

    await state.update_data(cart=cart_items)

    item = MENU[item_id]

    await callbackquery.answer(f"{item["name"]} savatga qo'shildi.")
