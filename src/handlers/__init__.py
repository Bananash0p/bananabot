from aiogram import Router, F
from aiogram.filters import CommandStart
from src.filters import ChatTypeFilter

from . import menu
from . import transaction


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
    router.callback_query.register(transaction.buy_proxy, F.data == "buy")

    # Регистрация транзакций
    
    return router
