from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tools import get_text_button


async def markup_back() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button(name='back'))
    return builder.as_markup(resize_keyboard=True)