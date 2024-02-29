from aiogram import Router

def setup_message_routers() -> Router:
    from . import start, add_recipes, del_recipes, viewing_recipes, any_unknow_message

    router = Router()
    router.include_router(start.router)
    router.include_router(viewing_recipes.router)
    router.include_router(add_recipes.router)
    router.include_router(del_recipes.router)
    router.include_router(any_unknow_message.router)
    
    # router.include_router(bot_messages.router)
    return router