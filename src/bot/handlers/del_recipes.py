from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User, Recipe
from tools import get_text_message, get_recipes, get_text_button
from bot.keyboards import markup_back
from bot.states import Admin
router = Router()


@router.message(Command('del'))
async def add_recipe(
    message: Message, state: FSMContext, command: CommandObject, session: AsyncSession, user: User
) -> None:
    recipes = '\n'.join([f'[{i.idpk}] {i.name}' for i in await get_recipes()])
    await message.answer(text=await get_text_message('send_me_num_recipe', recipes=recipes), reply_markup=await markup_back())
    await state.set_state(Admin.del_recipe)


@router.message(Admin.del_recipe)
async def del_recipe(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if message.text == await get_text_button(name='back'):
        await message.answer(text=await get_text_message('cancelled'), reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    if not message.text.isdigit():
        await message.answer(text=await get_text_message('send_me_num'))
        return
    recipe = await session.get(Recipe, int(message.text))
    if not recipe:
        await message.answer(text=await get_text_message('recipe_not_exist'))
        return
    await session.delete(recipe)
    await session.commit()
    await message.answer(text=await get_text_message('recipe_deleted'), reply_markup=ReplyKeyboardRemove())
    await state.clear()
    