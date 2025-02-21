from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src import states


# Обработчик кнопки "💵Купить"
async def buy_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    message_id = data.get("message_id")

    await callback.bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=message_id,
        caption="<b>🍌Введение кол-во прокси:</b>",
        parse_mode="HTML",
    )
    await state.set_state(states.user.Transaction.proxy)


# Обработчик выдачи прокси
