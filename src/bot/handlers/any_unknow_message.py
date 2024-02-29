from aiogram.types import Message
from aiogram import Router
from tools import get_text_message


router = Router()


@router.message()
async def any_unknow_message(
    message: Message
) -> None:
    await message.answer(text=await get_text_message('answer_on_unknow_message'))