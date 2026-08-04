from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers import (
    get_menu,
    refresh_cart,
    orders_are_open
)

from keyboards.customer import build_cart_keyboard

MENU = get_menu()

router = Router()


#VIEW CART ITEMS
@router.message(F.text=="🛒 Savat")
async def view_cart(message: Message,state: FSMContext):
    
    #Get cart
    data = await state.get_data()
    cart = data.get("cart",{})

    #If cart empty
    if not cart:
        await message.answer("🛒 Savatingiz bo'sh")
        return
    
    #If not empty, show cart
    text = "🛒 Savatingiz:\n\n"
    total = 0

    for item_id,amount in cart.items():
        item = MENU[item_id]
        text += f"{amount}x {item['name']} - {item['price']} so'm\n"
        total+=item["price"]*amount

    text += f"\n💰Jami: {total}so'm"
    
    #Inline keyboards to edit cart
    keyboard = build_cart_keyboard(cart)

    await message.answer(text, reply_markup=keyboard)


#CLEAR CART
@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cart={})

    await callback.message.edit_text(
        "🗑 Savat tozalandi."
    )

    await callback.answer()

#IF + IS PRESSED
@router.callback_query(F.data.startswith("plus:"))
async def plus_item(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split(":")[1])

    data = await state.get_data()
    cart = data.get("cart", {})

    cart[item_id] += 1

    await state.update_data(cart=cart)

    await refresh_cart(callback, state)

    await callback.answer()

#IF - IS PRESSED
@router.callback_query(F.data.startswith("minus:"))
async def minus_item(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split(":")[1])

    data = await state.get_data()
    cart = data.get("cart", {})

    cart[item_id] -= 1

    if cart[item_id] <= 0:
        del cart[item_id]

    await state.update_data(cart=cart)

    await refresh_cart(callback, state)

    await callback.answer()