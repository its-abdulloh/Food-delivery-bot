from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
)

from aiogram.fsm.context import FSMContext

from helpers import (
    ADMIN_ID,
    update_order_status,
    get_order_user,
    )

from states.admin import AdminCancelOrder


router = Router()

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