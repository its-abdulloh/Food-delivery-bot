from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from helpers import (
    ADMIN_ID,
    KITCHEN_ID,
    DRIVERS,
    update_order_status,
    get_order
)

router = Router()

#AFTER ASSIGN DRIVER PRESSED - SHOW DRIVERS
@router.callback_query(F.data.startswith("assign_driver:"))
async def show_drivers(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Not allowed", show_alert=True)
        return

    order_id = int(callback.data.split(":")[1])

    # build driver list dynamically
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🚚 {name}",
                    callback_data=f"set_driver:{order_id}:{driver_id}"
                )
            ]
            for driver_id, name in DRIVERS.items()
        ]
    )

    await callback.message.answer(
        "🚚 Qaysi haydovchiga beramiz?",
        reply_markup=keyboard
    )

    await callback.answer()

#ADMIN SETS DRIVER
@router.callback_query(F.data.startswith("set_driver:"))
async def set_driver(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Not allowed", show_alert=True)
        return

    _, order_id, driver_id = callback.data.split(":")
    order_id = int(order_id)
    driver_id = int(driver_id)

    order = get_order(order_id)

    if not order:
        await callback.answer("Order not found", show_alert=True)
        return

    update_order_status(order_id, "ASSIGNED_DRIVER")

    # notify driver
    await callback.bot.send_message(
        chat_id=driver_id,
        text=(
            "🚚 YANGI BUYURTMA\n\n"
            f"📦 Order #{order_id}\n"
            f"👤 {order['customer_name']}\n"
            f"📞 {order['phone']}\n\n"
            "📍 Yetkazib berishga tayyor!"
        )
    )

    # notify customer
    await callback.bot.send_message(
        chat_id=order["user_id"],
        text="🚚 Buyurtmangiz yo'lda!\n\n"
    )

    # update admin message
    await callback.message.edit_text(
        callback.message.text + "\n\n🚚 Driver tayinlandi",
        reply_markup=None
    )

    await callback.answer("Driver assigned")