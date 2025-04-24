import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from src.handlers import main_router

logging.basicConfig(level=logging.INFO)

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
