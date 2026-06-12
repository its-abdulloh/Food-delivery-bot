import asyncio
from aiogram import Bot
from config import TOKEN
from bot import dp   # import dispatcher from bot.py

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())