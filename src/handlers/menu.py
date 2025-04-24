from aiogram import Router, types
from src.keyboards import get_menu_keyboard

menu_router = Router()

@menu_router.callback_query(lambda c: c.data == "menu")
async def show_menu(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Главное меню:", reply_markup=get_menu_keyboard())
