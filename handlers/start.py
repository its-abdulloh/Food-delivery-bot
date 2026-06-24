from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
)
from aiogram.fsm.context import FSMContext

from states.registration import Registration

from helpers import (
    is_registered,
    main_keyboard,
    get_role,
    orders_are_open
)

from keyboards.admin import get_admin_keyboard
from keyboards.customer import main_keyboard,phone_keyboard

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
            "👨‍💼 Admin Paneli",
            reply_markup=get_admin_keyboard(orders_are_open())
        )
        return

    # KITCHEN
    if role == "kitchen":
        await message.answer(
            "👨‍🍳 Oshxona Paneli",
        )
        return

    # DRIVER
    if role == "driver":
        await message.answer(
            "🚚 Haydovchi Paneli",
        )
        return

    # CUSTOMER
    if is_registered(user_id):
        await message.answer(
            "👋 Xush kelibsiz!",
            reply_markup=main_keyboard
        )
        return

    await message.answer(
        "Assalomu alekum.\n"
        "Kuchli catering botiga xush kelibsiz.\n"
        "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring.",
        reply_markup=phone_keyboard
    )

    await state.set_state(
        Registration.waiting_for_phone
    )
