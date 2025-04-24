from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import re  # Для проверки названия комнаты

from src.db.database_manager import create_room, get_room_by_id

from src.keyboards import miniapp_keyboard

rooms_router = Router()


class RoomStates(StatesGroup):
    waiting_for_room_password = State()


class SelectRoomStates(StatesGroup):
    waiting_for_id = State()
    waiting_for_password = State()


@rooms_router.callback_query(lambda c: c.data == "select_room")
async def process_create_room(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("🔢<b>Введите id комнаты:</b>", parse_mode="HTML")
    await state.set_state(SelectRoomStates.waiting_for_id)


@rooms_router.message(SelectRoomStates.waiting_for_id)
async def process_room_id_input(message: types.Message, state: FSMContext):
    room_id = message.text.strip()

    if not room_id.isdigit():
        await message.answer("❌ <b>ID комнаты должен содержать только цифры.</b> Попробуйте снова.", parse_mode="HTML")
        return

    room = get_room_by_id(int(room_id))

    if not room:
        await message.answer("❌ <b>Комната с таким ID не найдена.</b> Попробуйте снова.", parse_mode="HTML")
        return

    await state.update_data(room_id=int(room_id))
    await message.answer("🔑 <b>Введите пароль:</b>", parse_mode="HTML")
    await state.set_state(SelectRoomStates.waiting_for_password)


@rooms_router.message(SelectRoomStates.waiting_for_password)
async def process_room_password_input(message: types.Message, state: FSMContext):
    room_password = message.text.strip()
    data = await state.get_data()
    room_id = data.get("room_id")

    room = get_room_by_id(room_id)

    if not room or room.password != room_password:
        await message.answer("❌ <b>Неверный пароль!</b> Попробуйте снова.", parse_mode="HTML")
        return

    await message.answer(f"✅ <b>Вы вошли в комнату!</b>\n🏠 ID: <code>{room_id}</code>", parse_mode="HTML", reply_markup=miniapp_keyboard())
    await state.clear()


@rooms_router.callback_query(lambda c: c.data == "create_room")
async def process_create_room(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("🔑 <b>Введите пароль для вашей комнаты:</b>", parse_mode="HTML")
    await state.set_state(RoomStates.waiting_for_room_password)


@rooms_router.message(RoomStates.waiting_for_room_password)
async def process_room_password(message: types.Message, state: FSMContext):
    room_password = message.text.strip()

    if len(room_password) < 6:
        await message.answer("❌ <b>Пароль должен содержать минимум 6 символов.</b> Попробуйте снова.",
                             parse_mode="HTML")
        return

    new_room = create_room(password=room_password)

    await message.answer(
        f"✅ <b>Комната создана!</b>\n"
        f"🔢 ID: <code>{new_room.session_id}</code>\n"
        f"🔑 Пароль: <code>{room_password}</code>",
        parse_mode="HTML"
    )

    await state.clear()
