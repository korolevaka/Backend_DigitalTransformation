import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.handlers import main_router

from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.include_router(main_router)

async def main():
    try:
        logging.info("🤖 <b>Бот запущен!</b> Ожидаем пользователей...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"⚠ <b>Ошибка при запуске бота:</b> {e}")

if __name__ == "__main__":
    asyncio.run(main())
