from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.fsm.context import FSMContext

from states.registration import Registration

from helpers import (
    is_registered,
    main_keyboard,
    get_role
)

from keyboards.admin import admin_keyboard
from keyboards.kitchen import kitchen_keyboard
from keyboards.driver import driver_keyboard

import logging

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


router = Router()

#START COMMAND THAT REGISTERS USERS
@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):

    user_id = message.from_user.id

    logger.info(f"User {user_id} sent: {message.text}")

    role = get_role(user_id)

    await state.clear()

    # ADMIN
    if role == "admin":
        await message.answer(
            "👨‍💼 Admin Panel",
            reply_markup=admin_keyboard
        )
        return

    # KITCHEN
    if role == "kitchen":
        await message.answer(
            "👨‍🍳 Kitchen Panel",
            reply_markup=kitchen_keyboard
        )
        return

    # DRIVER
    if role == "driver":
        await message.answer(
            "🚚 Driver Panel",
            reply_markup=driver_keyboard
        )
        return

    # CUSTOMER
    if is_registered(user_id):
        await message.answer(
            "👋 Xush kelibsiz!",
            reply_markup=main_keyboard()
        )
        return

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

    await message.answer(
        "Assalomu alekum.\n"
        "Kuchli catering botiga xush kelibsiz.\n"
        "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring.",
        reply_markup=phone_keyboard
    )

    await state.set_state(
        Registration.waiting_for_phone
    )
