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
from keyboards.customer import menu_item_keyboard,item_navigation_keyboard

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
    
    await state.set_state(AddCart.menu_pressed)
    await message.answer(
        "🍽 Bugungi Menu:",
        reply_markup=build_menu(MENU)
    )


#SHOW ITEM
@router.message(AddCart.menu_pressed,F.text.in_([item["name"] for item in MENU.values()]))
async def show_item(message:Message,state: FSMContext):
    for item_id,item in MENU.items():
        if message.text == item["name"]:
            await state.update_data(
                id=item_id,
                item=f"{item['name']}",
                price=f"{item["price"]}",
                amount=1
            )

            await message.answer(
                "Mahsulot miqdorini tanlang",
                reply_markup=item_navigation_keyboard
            )

            await state.set_state(AddCart.item_selected)
            await message.answer_photo(
                photo=item["photo_file_id"],
                caption=f"<b>{item['name']}</b>\n\n{item['name']} - {item['price']}\n Hammasi: {item["price"]}",
                parse_mode="HTML",
                reply_markup=menu_item_keyboard(item_id,1)
            )

@router.message(AddCart.item_selected,F.text == "⬅️ Orqaga")
async def back_to_menu(message: Message, state: FSMContext):
    await state.set_state(AddCart.menu_pressed)
    await message.answer(
        "🍽 Bugungi Menu:",
        reply_markup=build_menu(MENU)
    )

@router.message(AddCart.item_selected,F.text == "🛒 Savat")
async def show_cart(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", {})

    if not cart:
        await message.answer("🛒 Savatingiz bo'sh.")
        return

    text = "🛒 <b>Savatingiz:</b>\n\n"
    total = 0

    for item_id, amount in cart.items():
        item = MENU[item_id]
        subtotal = item["price"] * amount
        total += subtotal

        text += (
            f"{item['name']} × {amount} = {subtotal}\n"
        )

    text += f"\n<b>Jami: {total}</b>"

    await message.answer(text, parse_mode="HTML")

#INCREASE
@router.callback_query(F.data == "increase")
async def increase_amount(callbackquery: CallbackQuery,state:FSMContext):
    data = await state.get_data()

    amount = data.get("amount",1)+1

    await state.update_data(amount=amount)

    item_id= data.get("id")

    item_name = data.get("item")

    price = int(data.get("price"))

    total = price*amount

    await callbackquery.message.edit_caption(
        caption=(
            f"<b>{item_name}</b>\n\n"
            f"{item_name} - {price}\n"
            f"Hammasi: {total}"
            ),
        parse_mode="HTML",
        reply_markup=menu_item_keyboard(item_id,amount)
    )

    await callbackquery.answer()

    

#DECREASE
@router.callback_query(F.data=="decrease")
async def decrease_amount(callbackquery:CallbackQuery,state:FSMContext):
    data = await state.get_data()

    amount = data.get("amount")-1
    if amount==0:
        amount=1
        return

    await state.update_data(amount=amount)

    item_id= data.get("id")
    
    item_name = data.get("item")

    price = int(data.get("price"))

    total = price*amount

    await callbackquery.message.edit_caption(
        caption=(
            f"<b>{item_name}</b>\n\n"
            f"{item_name} - {price}\n"
            f"Hammasi: {total}"
            ),
            parse_mode="HTML",
        reply_markup=menu_item_keyboard(item_id,amount)
    )

    await callbackquery.answer()

# ADDS ITEM TO TEMP CART
@router.callback_query(F.data.startswith("add:"))
async def add_to_cart(callbackquery: CallbackQuery, state: FSMContext):
    if not orders_are_open():
        await callbackquery.answer(
            "Buyurtmalar yopilgan",
            show_alert=True
        )
        return
    item_id = int(callbackquery.data.split(":")[1])

    data = await state.get_data()
    cart_items = data.get("cart",{})

    item_id = data.get("id")
    amount = data.get("amount")


    #Add item to cart and its amount
    cart_items[item_id] = amount
    
    await state.update_data(cart=cart_items)

    item = MENU[item_id]

    await callbackquery.answer(f"{item['name']} savatga qo'shildi.")