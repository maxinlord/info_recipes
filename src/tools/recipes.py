from typing import Sequence
from sqlalchemy import select
from db import Recipe, Value
from init_db import _sessionmaker_for_func


async def get_recipes() -> Sequence[Recipe]:
    async with _sessionmaker_for_func() as session:
        result = await session.execute(select(Recipe))
        return result.scalars().all()
    
async def count_page_recipes(size_recipes: int | None = None) -> int:
    size_recipes = size_recipes or await get_size_recipes()
    async with _sessionmaker_for_func() as session:
        result = await session.execute(select(Recipe))
        len_recipes = len(result.scalars().all())
        remains = len_recipes % size_recipes
        return (len_recipes // size_recipes) + 1 if remains else len_recipes // size_recipes
    

async def get_row_keyboard() -> int:
    async with _sessionmaker_for_func() as session:
        result = await session.execute(select(Value.value).where(Value.name == 'row_keyboard'))
        return result.scalars().first()
    
async def get_size_recipes() -> int:
    async with _sessionmaker_for_func() as session:
        result = await session.execute(select(Value.value).where(Value.name == 'size_recipes'))
        return result.scalars().first()