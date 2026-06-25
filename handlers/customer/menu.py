from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers import (
    is_registered,
    build_menu,
    get_menu,
    orders_are_open
)

MENU = get_menu()

router = Router()


#SHOWS MENU
@router.message(F.text=="📋 Menu")
async def show_menu(message: Message):
    #If not registered
    if not is_registered(message.from_user.id):
        await message.answer("Iltimos avval ro'yxatdan o'ting. /start")
        return
    
    #if registered

    if not orders_are_open():
        await message.answer(
            "🔴 Bugun buyurtmalar qabul qilinmayapti."
        )
        return
    await message.answer(
        "🍽 Bugungi Menu:",
        reply_markup=build_menu(MENU)
    )


#ADDS ITEM TO TEMP CART
@router.callback_query(F.data.startswith("add:"))
async def add_to_cart(callbackquery: CallbackQuery, state: FSMContext):
    if not orders_are_open():
        await callbackquery.answer(
            "Buyurtmalar yopilgan",
            show_alert=True
        )
        return
    item_id = int(callbackquery.data.split(":")[1])

    cart = await state.get_data()
    cart_items = cart.get("cart",{})

    #Add item to cart and its number
    cart_items[item_id] = cart_items.get(item_id, 0) + 1
    
    await state.update_data(cart=cart_items)

    item = MENU[item_id]

    await callbackquery.answer(f"{item['name']} savatga qo'shildi.")