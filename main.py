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
from handlers.admin.assign_driver import router as assign_driver_router
from handlers.admin.open_close import router as open_close_router
from handlers.admin.menu import router as menu_admin_router

from handlers.kitchen.orders import router as orders_router
from handlers.driver.deliveries import router as deliveries_router


async def main():
    dp.include_router(start_router)
    dp.include_router(registration_router)
    dp.include_router(menu_router)
    dp.include_router(cart_router)
    dp.include_router(checkout_router)
    dp.include_router(order_router)
    dp.include_router(orders_router)
    dp.include_router(assign_driver_router)
    dp.include_router(open_close_router)
    dp.include_router(deliveries_router)
    dp.include_router(menu_admin_router)

    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())