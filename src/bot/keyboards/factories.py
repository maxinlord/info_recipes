from aiogram.filters.callback_data import CallbackData


class ProfileSettings(CallbackData, prefix="profile"):
    action: str = "change"
    value: str | None = None

    
class RecipeFactory(CallbackData, prefix="recipe"):
    action: str = "tap"
    id_recipe: int
    page: int

class ArrowFactory(CallbackData, prefix="arrow"):
    direction_arrow: str = "right"
    page: int