import asyncio
from aiogram import Bot
from config import TOKEN

from bot import dp   # import dispatcher from bot.py


from handlers.start import router as start_router
from handlers.customer.registration import router as registration_router
from handlers.customer.menu import router as menu_router
from handlers.customer.cart import router as cart_router
from handlers.customer.checkout import router as checkout_router

from handlers.admin.order import router as order_router



async def main():
    dp.include_router(start_router)
    dp.include_router(registration_router)
    dp.include_router(menu_router)
    dp.include_router(cart_router)
    dp.include_router(checkout_router)
    dp.include_router(order_router)

    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())