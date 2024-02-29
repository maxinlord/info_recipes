from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    add_recipe = State()
    del_recipe = State()