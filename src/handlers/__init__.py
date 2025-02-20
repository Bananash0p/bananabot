from aiogram import Router, F
from aiogram.filters import CommandStart
from src import states
from src.filters import ChatTypeFilter, TextFilter

from . import menu


def prepare_router() -> Router:
    router = Router()
    router.message.filter(ChatTypeFilter("private"))

    # Регистрация /start
    router.message.register(menu.start, CommandStart())

    # Регистрация callback-запросов
    router.callback_query.register(menu.show_bananas, F.data == "bananas")
    router.callback_query.register(menu.show_static, F.data == "static")
    router.callback_query.register(menu.show_resedential, F.data == "residential")
    router.callback_query.register(menu.go_back, F.data == "return")

    # Регистрация транзакций
    # СКОРО БУДЕТ!
    
    return router
