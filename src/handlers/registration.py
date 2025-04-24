from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.db.database_manager import create_player
from src.keyboards import get_menu_keyboard
import re

registration_router = Router()


class RegistrationStates(StatesGroup):
    waiting_for_fio = State()
    waiting_for_password = State()


@registration_router.callback_query(lambda c: c.data == "register")
async def process_register(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("✍ <b>Введите ваше ФИО:</b>", parse_mode="HTML")
    await state.set_state(RegistrationStates.waiting_for_fio)


def format_fio(fio: str) -> str:
    return " ".join(part.capitalize() for part in fio.split())


def is_valid_fio(fio: str) -> bool:
    parts = fio.split()
    if len(parts) != 3:
        return False
    pattern = r"^[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)?$"
    return all(re.match(pattern, part) for part in parts)


@registration_router.message(F.text, RegistrationStates.waiting_for_fio)
async def process_fio(message: types.Message, state: FSMContext):
    fio = message.text.strip()

    if not is_valid_fio(fio):
        await message.answer("⚠ <b>ФИО должно состоять из трёх частей и содержать только буквы.</b> Попробуйте снова.",
                             parse_mode="HTML")
        return

    formatted_fio = format_fio(fio)
    await state.update_data(fio=formatted_fio)
    await message.answer(
        f"✅ <b>Ваше ФИО сохранено как:</b> {formatted_fio}\n🔑 <b>Теперь введите пароль (минимум 8 символов):</b>",
        parse_mode="HTML")
    await state.set_state(RegistrationStates.waiting_for_password)


@registration_router.message(F.text, RegistrationStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    password = message.text.strip()

    if len(password) < 8:
        await message.answer("❌ <b>Пароль должен содержать минимум 8 символов.</b> Попробуйте снова.",
                             parse_mode="HTML")
        return

    data = await state.get_data()
    fio = data.get("fio")
    tg_id = message.from_user.id

    try:
        player = create_player(fio, password, tg_id)
        await message.answer(
            f"🎉 <b>Регистрация успешна!</b> Добро пожаловать, <b>{player.name}</b>! 🚀\n"
            f"🆔 Ваш Telegram ID: <code>{player.tg_id}</code>",
            reply_markup=get_menu_keyboard(),
            parse_mode="HTML"
        )
        await state.clear()
    except ValueError:
        await message.answer("⚠ <b>Пользователь с таким Telegram ID уже зарегистрирован.</b>", parse_mode="HTML")
