import asyncio
import logging

from aiogram import Router, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from helpers import build_menu, MENU
from helpers import (
    save_user,
    is_registered,
    main_keyboard,
    build_cart_keyboard,
    refresh_cart,
    create_order,
    ADMIN_ID,
    build_map_link,
    get_phone,
    update_order_status,
    get_order_user,
    )

from states.registration import Registration
from states.checkout import Checkout
from states.admin import AdminCancelOrder

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

#SETTING UP THE DISPATCHER
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


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

    for item_id,number in cart.items():
        item = MENU[item_id]
        text += f"{number}x {item['name']} - {item['price']} so'm\n"
        total+=item["price"]*number

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

#CHECKOUT PHASE
@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    cart = data.get("cart", {})

    if not cart:
        await callback.answer("Savat bo'sh")
        return
    
    await callback.message.answer(
        "Ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(
        Checkout.waiting_for_name
    )

    await callback.answer()


#RECIEVE NAME
@router.message(Checkout.waiting_for_name)
async def recieve_name(message: Message, state: FSMContext):

    await state.update_data(
        customer_name=message.text
    )

    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📍 Lokatsiyani yuborish",
                    request_location=True
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Lokatsiyangizni yuboring:",
        reply_markup=location_keyboard
    )

    await state.set_state(
        Checkout.waiting_for_location
    )

#AFTER THE SENDING THE LOCATION
@router.message(Checkout.waiting_for_location,F.location)
async def get_location(message:Message,state:FSMContext):

    #Saving the location
    await state.update_data(
        latitude = message.location.latitude,
        longitude = message.location.longitude
    )

    #Preparing the text
    data = await state.get_data()
    cart = data.get("cart", {})

    text = "📦 Buyurtma:\n\n"
    total = 0

    for item_id, qty in cart.items():
        item = MENU[item_id]
        text += f"{qty}x {item['name']}\n"
        total += item['price'] * qty

    text += f"\n💰 Jami: {total} so'm"

    text+=f"""

    Buyurtma tayyor:

    👤 {data['customer_name']}

    📍 Lokatsiya qabul qilindi

    Buyurtmani tasdiqlaysizmi?.
    """

    confirm_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data="confirm_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_order"
                )
            ]
        ]
    )

    #Confirming the order
    await message.answer(text,reply_markup=confirm_keyboard)


#IF VERIFY ORDER
@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery,state: FSMContext):

    await callback.message.answer(
        """
        💳 To'lov uchun karta:

        8600 0604 0244 3486

        Chek rasmini yuboring.
        """
    )

    await state.set_state(
        Checkout.waiting_for_payment
    )

    await callback.answer()


#IF CANCEL ORDER
@router.callback_query(F.data=="cancel_order")
async def cancel_order(callback: CallbackQuery,state: FSMContext):
    await state.clear()

    await callback.message.answer(
        "❌ Buyurtmangiz bekor qilindi.",
        reply_markup=main_keyboard()
    )

    await callback.answer("Bekor qilindi")

#WHEN THE PHOTO IS SENT
@router.message(Checkout.waiting_for_payment,F.photo)
async def payment_received(message: Message,state: FSMContext):

    #Get the highest quality image
    file_id = message.photo[-1].file_id

    await state.update_data(payment_file=file_id)

    user_id = message.from_user.id
    data = await state.get_data()
    cart = data.get("cart",{})
    order_id = create_order(data,message.from_user.id)

    #Build location and send to admin
    confirm_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data=f"confirm:{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=f"cancel:{order_id}"
                )
            ]
        ]
    )

    text = f"🆕 YANGI BUYURTMA #{order_id}\n"
    total = 0

    for item_id, qty in cart.items():
        item = MENU[item_id]
        text += f"\n{qty}x {item['name']}\n"
        total += item['price'] * qty

    text += f"\n💰 Jami: {total} so'm"

    text+=f"""

    👤 {data['customer_name']}
    📞 {get_phone(user_id)}

    📍 Location: {build_map_link(data.get("latitude"),data.get("longitude"))}

    💰 To'lov tasdiqlashi kutilmoqda
    """

    location_link = build_map_link(data.get('latitude'),data.get('longitude'))
    await message.bot.send_photo(
            ADMIN_ID,
            photo=file_id,
            caption=text
    ,reply_markup=confirm_keyboard)

    await message.answer(
        "✅ Chek qabul qilindi.\n\nAdmin tasdiqlashini kuting.",
        reply_markup=main_keyboard()
    )

    await state.clear()

#IF ADMIN CONFIRMS
@router.callback_query(F.data.startswith("confirm:"))
async def confirm(callback:CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Not allowed", show_alert=True)
        return

    order_id = int(callback.data.split(":")[1])

    update_order_status(order_id,"confirmed")

    user_id = get_order_user(order_id)
    await callback.bot.send_message(
        chat_id=user_id,
        text=(
            f"✅ Tolo'vingiz tasdiqlandi\n"
        )
    )

    await callback.message.edit_caption(
        callback.message.caption + "\n\n✅ Tasdiqlandi",
        reply_markup=None
    )

    await callback.answer("Order confirmed")

#IF ADMIN CANCELS
@router.callback_query(F.data.startswith("cancel:"))
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Not allowed", show_alert=True)
        return

    order_id = int(callback.data.split(":")[1])

    await state.update_data(
        order_id=order_id,
        admin_chat_id=callback.message.chat.id,
        admin_message_id=callback.message.message_id,
        original_caption=callback.message.caption
    )

    

    await callback.message.answer(
        f"Nega buyurtma #{order_id}ni bekor qilyapsiz?"
    )

    await state.set_state(AdminCancelOrder.waiting_for_reason)

    await callback.answer()

#IF INVALID REASON
@router.message(AdminCancelOrder.waiting_for_reason)
async def invalid_reason(message: Message):
    await message.answer(
        "Iltimos bekor qilish sababini matn ko'rinishida yuboring."
    )

#ASKING FOR WHY ADMIN CANCELED
@router.message(AdminCancelOrder.waiting_for_reason,F.text)
async def process_cancel_reason(
    message: Message,
    state: FSMContext
):
    reason = message.text

    data = await state.get_data()
    order_id = data["order_id"]
    admin_chat_id = data["admin_chat_id"]
    admin_message_id = data["admin_message_id"]
    caption = data["original_caption"]

    update_order_status(order_id, "CANCELED")

    user_id = get_order_user(order_id)

    await message.bot.send_message(
        user_id,
        f"""
❌ To'lovingiz bekor qilindi.

Sabab:
{reason}
"""
    )

    await message.bot.edit_message_caption(
        chat_id=admin_chat_id,
        message_id=admin_message_id,
        caption=caption + f"""

❌ Buyurtma bekor qilindi

Sabab:
{reason}
""",
        reply_markup=None
    )

    await message.answer(
        f"Buyurtma #{order_id} bekor qilindi."
    )

    await state.clear()

#ADD ROLES

#BUILD ADMIN KEYBOARD
# 📦 Active Orders
# 🍳 Kitchen Queue
# 🚗 Drivers
# 📋 Menu Management
# 📢 Broadcast
# 📊 Daily Summary


#KITCHEN UX
# 📋 Orders
# 📊 Summary
#DRIVER UX
#🚚 My Deliveries