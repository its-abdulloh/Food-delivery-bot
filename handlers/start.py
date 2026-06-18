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
    main_keyboard
)

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
