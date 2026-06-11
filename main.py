import asyncio
import logging
from dotenv import load_dotenv
import os

from aiogram import Bot, Router, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    logger.info(f"User {message.from_user.id} sent: {message.text}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Menu",callback_data="menu")]
    ])

    await message.answer("Assalomu alekum.\nKuchli catering botiga xush kelibsiz",reply_markup=keyboard)

@router.callback_query(lambda c:c.data=="menu")
async def menu_handler(callbackquery: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Osh",callback_data="dish_osh")],
        [InlineKeyboardButton(text="Shashlik",callback_data="dish_shashlik")],
        [InlineKeyboardButton(text="Manti",callback_data="dish_manti")],
        [InlineKeyboardButton(text="Lagmon",callback_data="dish_lagmon")]
    ])

    await callbackquery.message.edit_text("MENU:",reply_markup=keyboard)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())