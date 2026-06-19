from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.registration import Registration

from helpers import (
    save_user
)
from keyboards.customer import main_keyboard
import logging

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

router = Router()


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
        reply_markup=main_keyboard
    )


#IF DIDN'T USE THE BUTTON
@router.message(Registration.waiting_for_phone)
async def wrong_input(message: Message):
    await message.answer("Iltimos tugma yordamida raqamingizni ulashing!")
