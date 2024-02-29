import itertools
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from tools import get_text_button, get_size_recipes, get_row_keyboard
from .factories import RecipeFactory, ArrowFactory
from db import Recipe


def reply_builder(
    text: str | list[str],
    sizes: int | list[int] = 2,
    **kwargs
) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()

    text = [text] if isinstance(text, str) else text
    sizes = [sizes] if isinstance(sizes, int) else sizes

    [
        builder.button(text=txt)
        for txt in text
    ]

    builder.adjust(*sizes)
    return builder.as_markup(resize_keyboard=True, **kwargs)


def inline_builder(
    text: str | list[str],
    callback_data: str | list[str],
    sizes: int | list[int] = 2,
    **kwargs
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    text = [text] if isinstance(text, str) else text
    callback_data = [callback_data] if isinstance(
        callback_data, str) else callback_data
    sizes = [sizes] if isinstance(sizes, int) else sizes

    [
        builder.button(text=txt, callback_data=cb)
        for txt, cb in zip(text, callback_data)
    ]

    builder.adjust(*sizes)
    return builder.as_markup(**kwargs)


async def recipe_inline_builder(
    recipes: list[Recipe],
    row_keyboard: int | None = None,
    page: int = 1,
    size_recipes: int | None = None
) -> InlineKeyboardBuilder:
    row_keyboard = row_keyboard or await get_row_keyboard()
    size_recipes = size_recipes or await get_size_recipes()
    builder = InlineKeyboardBuilder()
    start = (page-1) * size_recipes
    stop = start + size_recipes
    sliced_recipes = itertools.islice(recipes, start, stop)
    count_recipes = 0
    for recipe in sliced_recipes:
        builder.button(text=await get_text_button(name='pattern_button_name_recipe', name_r=recipe.name),
                       callback_data=RecipeFactory(id_recipe=recipe.idpk, page=page))
        count_recipes += 1

    whole_pairs = count_recipes//row_keyboard
    remainder = count_recipes % row_keyboard
    row = [row_keyboard for _ in range(
        whole_pairs)] + [remainder] if remainder else [row_keyboard for _ in range(whole_pairs)]

    builder.button(text=await get_text_button('arrow_left'), callback_data=ArrowFactory(direction_arrow='left', page=page))
    builder.button(text=await get_text_button('arrow_right'), callback_data=ArrowFactory(page=page))
    builder.adjust(*row, 2)

    return builder.as_markup()
