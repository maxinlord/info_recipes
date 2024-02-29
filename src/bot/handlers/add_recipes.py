from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User, Recipe
from tools import get_text_message, get_text_button
from bot.keyboards import markup_back
from bot.states import Admin
router = Router()


@router.message(Command('add'))
async def add_recipe(
    message: Message, state: FSMContext, command: CommandObject, session: AsyncSession, user: User
) -> None:
    await message.answer(text=await get_text_message('send_me_recipe'), reply_markup=await markup_back())
    await state.set_state(Admin.add_recipe)


@router.message(Admin.add_recipe)
async def get_recipe_from_user(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if message.text == await get_text_button('back'):
        await message.answer(text=await get_text_message('cancelled'), reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    name_recipe = message.text.split('\n')[0]
    recipe = '\n'.join(message.text.split('\n')[1:])
    session.add(Recipe(name=name_recipe, text=recipe))
    await session.commit()
    await message.answer(text=await get_text_message('recipe_added'), reply_markup=ReplyKeyboardRemove())
    await state.clear()
    