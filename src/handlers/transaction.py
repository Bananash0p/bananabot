import requests

from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from src import states

# Обработчик кнопки "💵Купить"
async def buy_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    message_id = data.get('message_id')

    await callback.bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=message_id,
        caption="<b>🍌Введение кол-во прокси:</b>",
        parse_mode="HTML"
    )
    await state.set_state(states.user.Transaction.proxy)


# Обработчик выдачи прокси
async def give_proxy(message: Message, state: FSMContext) -> None:
    txt_url = "https://gold-quickest-bird-528.mypinata.cloud/ipfs/bafkreicyxuugcprdyahk7net7mehmlm3yisosuc5enxhske74qigffnaey"
    response = requests.get(txt_url)
    document = BufferedInputFile(response.content, filename="proxies.txt")

    await message.answer_document(document=document)


