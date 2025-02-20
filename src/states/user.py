from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    main = State()
    bananas = State()
    static = State()
    resedential = State()
    mobile = State()

class Transaction(StatesGroup):
    buy = State()
    proxy = State()