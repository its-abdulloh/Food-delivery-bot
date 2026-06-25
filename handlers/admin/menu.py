from aiogram import Router,F
from aiogram.types import (
    Message,
)
from aiogram.fsm.context import FSMContext

from states.admin import MenuState
from helpers import clear_menu,add_menu_item


router = Router()

@router.message(F.text == "📋 Bugungi Menu")
async def menu_button(message: Message, state: FSMContext):
    await message.answer(
        "Bugungi menyuni yuboring:\n\n"
        "Plov - 30000\n"
        "Manti - 25000\n"
        "Lag'mon - 35000\n"
        "Salat - 15000"
    )

    await state.set_state(MenuState.waiting_for_menu)

@router.message(MenuState.waiting_for_menu)
async def save_menu(message: Message, state: FSMContext):
    try:
        lines = message.text.strip().split("\n")

        clear_menu()

        for line in lines:
            name, price = line.split("-")

            name = name.strip()
            price = int(price.strip())

            add_menu_item(name, price)

        await message.answer("✅ Bugungi menu saqlandi.")
        await state.clear()

    except Exception:
        await message.answer(
            "❌ Format noto'g'ri.\n\n"
            "Misol:\n"
            "Plov - 30000\n"
            "Manti - 25000"
        )