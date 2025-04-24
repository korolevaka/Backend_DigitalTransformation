from aiogram import Router, types
from aiogram.types import InputFile
from src.keyboards import get_rules_keyboard

# Создаем роутер для обработки запроса на правила
rules_router = Router()

# Обработчик нажатия на кнопку "📖 Правила игры"
@rules_router.message(lambda message: message.text == "📖 Правила игры")
async def send_game_rules(message: types.Message):
    # Путь к изображениям относительно папки проекта
    photo_1 = InputFile("src/images/правила.png")  # Путь к первому изображению
    photo_2 = InputFile("src/images/роли.png")  # Путь ко второму изображению

    # Отправляем изображения с правилами
    await message.answer("📜 <b>Правила игры:</b>", parse_mode="HTML", reply_markup=get_rules_keyboard())
    await message.answer_photo(photo_1, caption="Правила")
    await message.answer_photo(photo_2, caption="Роли")
