from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from helpers import (
    DRIVERS,
    ADMIN_ID,
    update_order_status,
    get_order_user
)

router = Router()

@router.callback_query(F.data.startswith("picked_up:"))
async def picked_up(callback: CallbackQuery):
    if callback.from_user.id not in DRIVERS.keys:
        await callback.answer("Not allowed", show_alert=True)
        return
    
    order_id = int(callback.data.split(":")[1])

    #Update driver message
    delivered_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚚 Jo'natmani yetkazib berdm",
                    callback_data=f"delivered:{order_id}"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        callback.message.text + "\n\n🚚 Buyurtma olindi",
        reply_markup=delivered_keyboard
    )
    
    # notify customer
    await callback.bot.send_message(
        chat_id=get_order_user(order_id),
        text="🚚 Buyurtmangiz yo'lda!\n\n"
    )

    #notify admin
    await callback.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🚚 Buyurtma #{order_id} yo'lda!"
    )

    update_order_status(order_id, "PICKED_UP")

    await callback.answer("Buyurtma yo'lda")



@router.callback_query(F.data.startswith("delivered:"))
async def delivered(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[1])

    await callback.message.edit_text(
        callback.message.text + "\n\n✅ Buyurtma yetib bordi",
        reply_markup=None
    )
    
    # notify customer
    await callback.bot.send_message(
        chat_id=get_order_user(order_id),
        text="🚚 Buyurtmangiz yetb keldi!\n\n"
    )

    #notify admin
    await callback.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🚚 Buyurtma #{order_id} yetb bordi!"
    )

    update_order_status(order_id, "DELIVERED")

    await callback.answer("Buyurtma yetib bordi")