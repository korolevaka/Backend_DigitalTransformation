from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔑 Войти", callback_data="login")],
        [InlineKeyboardButton(text="📝 Зарегистрироваться", callback_data="register")]
    ])

def get_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Создать комнату", callback_data="create_room")],
        [InlineKeyboardButton(text="📌 Выбрать комнату", callback_data="select_room")]
    ])

def get_rules_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("📖 Правила игры")]],
        resize_keyboard=True
    )

def miniapp_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Играть", web_app=WebAppInfo(url="https://cherubscodes.github.io/"))]])
