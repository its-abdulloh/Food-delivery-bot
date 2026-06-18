import asyncio
from aiogram import Bot
from config import TOKEN
from bot import dp   # import dispatcher from bot.py
from handlers.start import router as start_router
from handlers.registration import router as registration_router
from handlers.menu import router as menu_router
from handlers.cart import router as cart_router

dp.include_router(start_router)
dp.include_router(registration_router)
dp.include_router(menu_router)
dp.include_router(cart_router)

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())