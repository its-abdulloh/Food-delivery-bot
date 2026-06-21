from aiogram import Router, F
from aiogram.types import (
    Message,
)

from helpers import (
    ADMIN_ID,
    set_orders_open,
)

from keyboards.admin import get_admin_keyboard

router = Router()

@router.message(F.text == "🟢 Open Orders")
async def open_orders_handler(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    set_orders_open(True)

    await message.answer(
        "🟢 Buyurtmalar ochildi",
        reply_markup=get_admin_keyboard(True)
    )

@router.message(F.text == "🔴 Close Orders")
async def close_orders_handler(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    set_orders_open(False)

    await message.answer(
        "🔴 Buyurtmalar yopildi",
        reply_markup=get_admin_keyboard(False)
    )