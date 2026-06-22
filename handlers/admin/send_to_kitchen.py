# from aiogram import Router, F
# from aiogram.types import (
#     Message,
# )

# from helpers import (
#     ADMIN_ID,
#     generate_kitchen_summary,
#     MENU,
#     KITCHEN_ID,
#     update_status_where,
#     orders_are_open
# )

# from keyboards.admin import get_admin_keyboard

# router = Router()

# @router.message(F.text=="👨‍🍳 Oshxonaga jo'natish")
# async def send_to_kitchen(message: Message):
    
#     if message.from_user.id != ADMIN_ID:
#         return
    
#     summary = generate_kitchen_summary()

#     summary_text = "BUGUNGU BUYURTMA📋:\n\n"

#     for item_id, qty in summary.items():
#         summary_text+=f"{MENU[item_id]} - {qty}\n"
    
#     message.bot.send_message(
#         KITCHEN_ID,
#         text=summary_text
#     )

#     update_status_where("CONFIRMED","IN_KITCHEN")

#     message.answer(
#         text="Oshxonaga jo'natildi",
#         reply_markup=get_admin_keyboard(orders_are_open())
#     )
    


    
    