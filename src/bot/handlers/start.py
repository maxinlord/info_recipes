from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
from tools import get_text_message, get_recipes
from bot.keyboards import recipe_inline_builder


router = Router()


@router.message(CommandStart())
async def command_start(
    message: Message, state: FSMContext, command: CommandObject, session: AsyncSession, user: User
) -> None:
    recipes = await get_recipes()
    await message.answer(text=await get_text_message('start_message'), reply_markup=await recipe_inline_builder(recipes=recipes))
    


