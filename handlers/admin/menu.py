from aiogram import Router,F
from aiogram.types import (
    Message,
)
from aiogram.fsm.context import FSMContext

from states.admin import AddItem,DeleteItem,ShowMenu
from helpers import clear_menu,add_menu_item,get_menu,delete_menu_item,is_admin,orders_are_open
from keyboards.admin import admin_menu_keyboard,delete_menu_keyboard,menu_items_keyboard,get_admin_keyboard



router = Router()

@router.message(F.text == "📋 Menu boshqarish")
async def menu_button(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q!")
        return
    await message.answer(
        "Menu Management:",
        reply_markup=admin_menu_keyboard()
    )

#BACK BUTTON
@router.message(F.text == "🔙 Orqaga")
async def admin_back(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    await message.answer(
        "Admin panel:",
        reply_markup=get_admin_keyboard(orders_are_open())
    )

#ADD ITEM
@router.message(F.text == "➕ Qo'shish")
async def save_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q!")
        return
    await state.set_state(AddItem.waiting_for_name)
    await message.answer("Ovqat nomini kiriting:")

@router.message(AddItem.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q!")
        return
    await state.update_data(name=message.text)

    await state.set_state(AddItem.waiting_for_price)
    await message.answer(
        text="Narxini kiriting:",
        reply_markup=None
    )

@router.message(AddItem.waiting_for_price)
async def get_price(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q!")
        return
    if not message.text.isdigit():
        await message.answer("Faqat son kiriting.")
        return

    await state.update_data(price=int(message.text))

    await state.set_state(AddItem.waiting_for_photo)
    await message.answer("Ovqat rasmini yuboring:")


@router.message(AddItem.waiting_for_photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q!")
        return
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

#DELETE ITEM
@router.message(F.text == "🗑 O'chirish")
async def delete_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q!")
        return
    menu = get_menu()

    if not menu:
        await message.answer("Menu bo'sh.")
        return

    await state.set_state(DeleteItem.waiting_for_item)

    await message.answer(
        "O'chirmoqchi bo'lgan ovqatni tanlang:",
        reply_markup=delete_menu_keyboard(menu)
    )

@router.message(DeleteItem.waiting_for_item, F.text == "🔙 Orqaga")
async def back_from_delete(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Menu Management:",
        reply_markup=admin_menu_keyboard()
    )

@router.message(DeleteItem.waiting_for_item)
async def delete_item(message: Message, state: FSMContext):
    menu = get_menu()

    # Check if the selected name exists
    selected_name = message.text
    names = [item["name"] for item in menu.values()]

    if selected_name not in names:
        await message.answer("Iltimos, ro'yxatdan ovqatni tanlang.")
        return

    # Delete from database
    delete_menu_item(selected_name)

    await message.answer(
        f"✅ {selected_name} menyudan o'chirildi.",
        reply_markup=admin_menu_keyboard()
    )

    await state.clear()

#CLEAR MENU
@router.message(F.text == "🧹 Tozalash")
async def clear_menu(message:Message):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q!")
        return
    clear_menu()

    await message.answer("Menu tozalandi!")


#SHOW MENU
@router.message(F.text == "📋 Menu")
async def show_menu(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ruxsat yo'q!")
        return
    menu = get_menu()

    if not menu:
        await message.answer("📭 Menu bo'sh.")
        return

    await state.set_state(ShowMenu.waiting_for_item)

    await message.answer(
        "Ovqatni tanlang:",
        reply_markup=menu_items_keyboard(menu)
    )

@router.message(ShowMenu.waiting_for_item)
async def show_selected_item(message: Message, state: FSMContext):
    menu = get_menu()

    for item in menu.values():
        if item["name"] == message.text:
            await message.answer_photo(
                photo=item["photo_file_id"],
                caption=(
                    f"🍽 <b>{item['name']}</b>\n"
                    f"💰 {item['price']} so'm"
                ),
                parse_mode="HTML"
            )
            return

    await message.answer("Iltimos, ro'yxatdan ovqatni tanlang.")