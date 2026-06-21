from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext

from states.checkout import Checkout

from helpers import (
    MENU,
    build_map_link,
    ADMIN_ID,
    get_phone,
    create_order,
    orders_are_open
)

from keyboards.customer import main_keyboard

router = Router()


#CHECKOUT PHASE
@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):

    if not orders_are_open():
        await callback.message.answer(
            "🔴 Bugun buyurtmalar qabul qilinmayapti."
        )
        return
    
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
        reply_markup=main_keyboard
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
