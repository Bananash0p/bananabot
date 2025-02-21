from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src import states


async def create_keyboard(state: FSMContext) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    current_state = await state.get_state()

    match current_state:
        case states.user.Menu.main:
            builder.button(text="🛜Прокси", callback_data="bananas")
            builder.button(text="🇬🇧ENG", callback_data="eng_language")
            builder.adjust(1)
        case states.user.Menu.bananas:
            builder.button(text="🗿Static", callback_data="static")
            builder.button(text="🏡Residential", callback_data="residential")
            builder.button(text="☎️Mobile", callback_data="residential")
            builder.button(text="🔙 Назад", callback_data="return")
            builder.adjust(3, 1)
        case states.user.Menu.static | states.user.Menu.resedential | states.user.Menu.mobile:
            builder.button(text="💵Купить", callback_data="buy")
            builder.button(text="🔙 Назад", callback_data="return")
            builder.adjust(1)

    return builder.as_markup()


# Обработчик  "🔙Назад"
async def go_back(callback: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()

    match current_state:
        case states.user.Menu.bananas:
            await start(callback.message, state)
        case states.user.Menu.static | states.user.Menu.resedential | states.user.Menu.mobile:
            await show_bananas(callback, state)


# Обработчик /start
async def start(data: Message | CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(states.user.Menu.main)
    
    png_url = "https://gold-quickest-bird-528.mypinata.cloud/ipfs/bafkreie3xabthu6wiac7huqzunojalgivxeni3rwqoabbrnfwmu4maynqu"
    keyboard = await create_keyboard(state)
    
    if current_state == states.user.Menu.bananas:
        state_data = await state.get_data()
        message_id = state_data.get("message_id")
        
        await data.bot.edit_message_caption(
            chat_id=data.chat.id,
            message_id=message_id,
            caption="<b>🍌BANANA SHOP -</b> Ваш ЛУЧШИЙ поставщий прокси!",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    else:
        sent_message = await data.answer_photo(
            png_url,
            caption="<b>🍌BANANA SHOP -</b> Ваш ЛУЧШИЙ поставщий прокси!",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        await state.update_data(message_id=sent_message.message_id, chat_id=data.chat.id)


# Обработчик кнопки "🛜Прокси"
async def show_bananas(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.user.Menu.bananas)

    data = await state.get_data()
    message_id = data.get("message_id")
    keyboard = await create_keyboard(state)

    await callback.bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=message_id,
        caption="<b>🍌Каталог</b>\n\nВыберите сорт:",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# Обработчик кнопки "🗿Static"
async def show_static(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.user.Menu.static)

    data = await state.get_data()
    message_id = data.get("message_id")
    keyboard = await create_keyboard(state)

    await callback.bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=message_id,
        caption="<b>🍌О банане</b>\n\n• Протокол: HTTPS🔒/ SOCKS5🛡️\n• Скорость: 100 Мбит/с⚡\n• Формат: IPv4\n• Цена: Договоримся🤝",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# Обработчик кнопки "🏡Residential"
async def show_resedential(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.user.Menu.resedential)

    data = await state.get_data()
    message_id = data.get("message_id")
    keyboard = await create_keyboard(state)

    await callback.bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=message_id,
        caption="<b>🍌О банане</b>\n\n• Протокол: HTTPS🔒/ SOCKS5🛡️\n• Скорость: 100 Мбит/с⚡\n• Формат: IPv4\n• Цена: Договоримся🤝",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# Обработчик кнопки "☎️Mobile"
async def show_mobile(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.user.Menu.static)

    data = await state.get_data()
    message_id = data.get("message_id")
    keyboard = await create_keyboard(state)

    await callback.bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=message_id,
        caption="<b>🍌О банане</b>\n\n• Протокол: HTTPS🔒/ SOCKS5🛡️\n• Скорость: 100 Мбит/с⚡\n• Формат: IPv4\n• Цена: Договоримся🤝",
        reply_markup=keyboard,
        parse_mode="HTML",
    )



