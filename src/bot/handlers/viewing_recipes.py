from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import User, Recipe
from tools import get_text_message, get_recipes, count_page_recipes
from bot.keyboards import recipe_inline_builder, inline_back
from bot.keyboards import ArrowFactory, RecipeFactory

router = Router()


@router.callback_query(ArrowFactory.filter(F.direction_arrow == "right"))
async def process_turn_right(query: CallbackQuery, callback_data: ArrowFactory, state: FSMContext, session: AsyncSession, user: User) -> None:
    q_page = await count_page_recipes()
    page = callback_data.page
    page = page + 1 if page < q_page else 1
    await query.message.edit_reply_markup(reply_markup=await recipe_inline_builder(page=page, recipes=await get_recipes()))


@router.callback_query(ArrowFactory.filter(F.direction_arrow == "left"))
async def process_turn_left(query: CallbackQuery, callback_data: ArrowFactory, state: FSMContext, session: AsyncSession, user: User) -> None:
    q_page = await count_page_recipes()
    page = callback_data.page
    page = page - 1 if page > 1 else q_page
    await query.message.edit_reply_markup(reply_markup=await recipe_inline_builder(page=page, recipes=await get_recipes()))

@router.callback_query(ArrowFactory.filter(F.direction_arrow == "back"))
async def process_back_to_menu(query: CallbackQuery, callback_data: ArrowFactory, state: FSMContext, session: AsyncSession, user: User) -> None:
    await query.message.edit_text(text=await get_text_message('start_message'), reply_markup=await recipe_inline_builder(page=callback_data.page, recipes=await get_recipes()))

@router.callback_query(RecipeFactory.filter(F.action == "tap"))
async def process_viewing_recipes(query: CallbackQuery, callback_data: RecipeFactory, state: FSMContext, session: AsyncSession, user: User) -> None:
    res = await session.execute(select(Recipe).where(Recipe.idpk == callback_data.id_recipe))
    recipe = res.scalars().first()
    await query.message.edit_text(await get_text_message(name='viewing_recipe', 
                                                         description=recipe.text, 
                                                         name_r=recipe.name), reply_markup=await inline_back(page=callback_data.page))
