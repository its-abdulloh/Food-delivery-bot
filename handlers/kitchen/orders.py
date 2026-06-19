from aiogram import Router, F
from aiogram.types import CallbackQuery

from helpers import (
    ADMIN_ID,
    get_order,
    update_order_status,
    KITCHEN_ID
)

router = Router()


@router.callback_query(F.data.startswith("prepared:"))
async def mark_prepared(callback: CallbackQuery):

    if callback.from_user.id != KITCHEN_ID:
        await callback.answer("Not allowed", show_alert=True)
        return

    order_id = int(callback.data.split(":")[1])

    order = get_order(order_id)

    if not order:
        await callback.answer("Order not found", show_alert=True)
        return

    update_order_status(order_id, "PREPARED")

    # notify admin
    await callback.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"👨‍🍳 BUYURTMA #{order_id} tayyor bo'ldi!\n"
            "🚚 Endi haydovchi tayinlash mumkin."
        )
    )

    # notify customer
    await callback.bot.send_message(
        chat_id=order["user_id"],
        text=(
            "✅ Buyurtmangiz tayyor!\n\n"
            "🚚 Tez orada yetkazib beriladi."
        )
    )

    # update kitchen message
    await callback.message.edit_text(
        callback.message.text + "\n\n✅ Tayyor bo'ldi",
        reply_markup=None
    )

    await callback.answer("Marked as prepared")

