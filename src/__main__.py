import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from bot.handlers import setup_message_routers
from bot.middlewares import DBSessionMiddleware, CheckUser

from db import Base
from init_db import _sessionmaker, _engine
import config


async def on_startup(_engine: AsyncEngine) -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   


async def on_shutdown(session: AsyncSession) -> None:
    await session.close()



async def main() -> None:
    
    
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(config.BOT_TOKEN, default=default)
    dp = Dispatcher(_engine=_engine, storage=MemoryStorage())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.callback_query.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    
    dp.message.middleware(CheckUser()) 
    dp.callback_query.middleware(CheckUser()) 

    message_routers = setup_message_routers()
    dp.include_router(message_routers)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

