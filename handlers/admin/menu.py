from aiogram import Router,F
from aiogram.types import (
    Message,
)
from aiogram.fsm.context import FSMContext

from keyboards.admin import get_menu_admin_keyboard
from states.admin import AddMenuItem

router = Router()

@router.message(F.text == "📋 MENU")
async def open_menu_admin(message: Message, state: FSMContext):

    await state.clear()  # important: reset any FSM

    await message.answer(
        "🍽 MENU ADMIN",
        reply_markup=get_menu_admin_keyboard()
    )