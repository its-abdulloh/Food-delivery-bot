from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers import (
    is_registered,
    build_menu,
    get_menu,
    orders_are_open
)

from states.order import AddCart
from keyboards.customer import menu_item_keyboard

MENU = get_menu()

router = Router()


#SHOWS MENU
@router.message(F.text=="📋 Menu")
async def show_menu(message: Message,state:FSMContext):
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
    
    state.set_state(AddCart.menu_pressed)
    await message.answer(
        "🍽 Bugungi Menu:",
        reply_markup=build_menu(MENU)
    )


#SHOW ITEM
@router.message(AddCart.menu_pressed)
async def show_item(message:Message,state: FSMContext):
    for item_id,item in MENU.items():
        if message.text == item["name"]:
            state.update_data(item=f"{item['name']}",amount=1)
            await message.answer_photo(
                photo=item["photo"],
                caption=f"<b>{item['name']}<b>\n\n{item['name']} - {item['price']}\n Hammasi: {item["price"]}",
                reply_markup=menu_item_keyboard(item_id,1)
            )

#INCREASE

#DECREASE

#ADDS ITEM TO TEMP CART
# @router.callback_query(F.data.startswith("add:"))
# async def add_to_cart(callbackquery: CallbackQuery, state: FSMContext):
#     if not orders_are_open():
#         await callbackquery.answer(
#             "Buyurtmalar yopilgan",
#             show_alert=True
#         )
#         return
#     item_id = int(callbackquery.data.split(":")[1])

#     cart = await state.get_data()
#     cart_items = cart.get("cart",{})

#     #Add item to cart and its number
#     cart_items[item_id] = cart_items.get(item_id, 0) + 1
    
#     await state.update_data(cart=cart_items)

#     item = MENU[item_id]

#     await callbackquery.answer(f"{item['name']} savatga qo'shildi.")