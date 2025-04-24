from aiogram import Router
from .start import start_router
from .registration import registration_router
from .login import login_router
from .rooms import rooms_router
from .menu import menu_router
from .game_rules import rules_router

main_router = Router()

main_router.include_router(start_router)
main_router.include_router(registration_router)
main_router.include_router(login_router)
main_router.include_router(rooms_router)
main_router.include_router(menu_router)
main_router.include_router(rules_router)
