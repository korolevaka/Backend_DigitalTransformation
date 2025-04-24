from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, InputMediaPhoto

from src.db.database_manager import get_image
from src.keyboards import get_start_keyboard

start_router = Router()

@start_router.message(Command("start"))
async def send_welcome(message: types.Message):
    image1 = get_image("правила1")
    image2 = get_image("правила2")

    if image1 and image2:
        photo1 = BufferedInputFile(image1.image_data, filename="правила1.png")
        photo2 = BufferedInputFile(image2.image_data, filename="правила2.png")

        media = [
            InputMediaPhoto(media=photo1),
            InputMediaPhoto(media=photo2),
        ]

        await message.answer_media_group(media)
    else:
        await message.answer("Одно или оба изображения не найдены.")

    await message.answer(
        "🎮 <b>Добро пожаловать в игру «Цифровая трансформация»!</b> 🚀\n\n"
        "Здесь вы сможете управлять процессами трансформации компании. 🏢\n\n"
        "🔑 Для начала игры <b>войдите</b> или <b>зарегистрируйтесь</b>.",
        parse_mode="HTML",
        reply_markup=get_start_keyboard()
    )
