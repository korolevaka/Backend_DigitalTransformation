from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.db.database_manager import get_player_by_login
from src.keyboards import get_menu_keyboard
import re

login_router = Router()


class LoginStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()


@login_router.callback_query(lambda c: c.data == "login")
async def process_login(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("🔑 Введите ваш <b>логин</b>:", parse_mode="HTML")
    await state.set_state(LoginStates.waiting_for_login)


@login_router.message(LoginStates.waiting_for_login)
async def process_login_data(message: types.Message, state: FSMContext):
    login = message.text.strip()

    if len(login) < 3:
        await message.answer("⚠ Логин должен содержать хотя бы 3 символа. Попробуйте снова.", parse_mode="HTML")
        return

    await state.update_data(login=login)
    await message.answer("🔑 Теперь введите ваш <b>пароль</b>:", parse_mode="HTML")
    await state.set_state(LoginStates.waiting_for_password)


@login_router.message(LoginStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    password = message.text.strip()

    if len(password) < 6:
        await message.answer("⚠ Пароль должен содержать минимум 6 символов. Попробуйте снова.", parse_mode="HTML")
        return

    data = await state.get_data()
    login = data.get("login")

    player = get_player_by_login(login)
    if player and player.password == password:  # Сравниваем пароль из базы данных
        await message.answer(f"✅ <b>Вход выполнен!</b> Добро пожаловать, <b>{login}</b>!", parse_mode="HTML",
                             reply_markup=get_menu_keyboard())
    else:
        await message.answer("⚠ Логин или пароль неверный.", parse_mode="HTML")

    await state.clear()
