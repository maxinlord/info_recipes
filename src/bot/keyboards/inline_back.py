from aiogram.utils.keyboard import InlineKeyboardBuilder
from tools import get_text_button
from .factories import ArrowFactory


async def inline_back(page: int) -> InlineKeyboardBuilder:

    builder = InlineKeyboardBuilder()
    builder.button(text=await get_text_button(name='back'),
                   callback_data=ArrowFactory(direction_arrow='back', page=page))
    return builder.as_markup()
