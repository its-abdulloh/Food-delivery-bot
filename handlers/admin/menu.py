from aiogram import Router,F
from aiogram.types import (
    Message,
)
from aiogram.fsm.context import FSMContext

from states.admin import AddItem
from helpers import clear_menu,add_menu_item,parse_line
from keyboards.admin import admin_menu_keyboard



router = Router()

@router.message(F.text == "📋 Bugungi Menu")
async def menu_button(message: Message, state: FSMContext):
    await message.answer(
        "Menu Management:",
        reply_markup=admin_menu_keyboard()
    )

@router.message(F.text == "➕ Qo'shish")
async def save_menu(message: Message, state: FSMContext):
    await state.set_state(AddItem.waiting_for_name)
    await message.answer("Ovqat nomini kiriting:")

@router.message(AddItem.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await state.set_state(AddItem.waiting_for_price)
    await message.answer("Narxini kiriting:")

@router.message(AddItem.waiting_for_price)
async def get_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Faqat son kiriting.")
        return

    await state.update_data(price=int(message.text))

    await state.set_state(AddItem.waiting_for_photo)
    await message.answer("Ovqat rasmini yuboring:")

@router.message(AddItem.waiting_for_photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id

    data = await state.get_data()

    name = data["name"]
    price = data["price"]

    # Save to database
    add_menu_item(
        name=name,
        price=price,
        photo=photo
    )

    await message.answer(
        f"✅ {name} menyuga qo'shildi!"
    )

    await state.clear()

@router.message(AddItem.waiting_for_photo)
async def photo_required(message: Message):
    await message.answer("Iltimos, rasm yuboring.")