import os
import asyncio
from aiogram import Bot, Dispatcher, Router,types
from aiogram.client import bot
from dotenv import load_dotenv
from handlers import reg_routes
from database.models import BaseModel
from middlewares import reg_middlewares
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

token = os.getenv('BOT_TOKEN')

async def init_model(engine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)



async def main():
    bot = Bot(token=token)
    dp = Dispatcher()

    engine = create_async_engine(
        url="sqlite+aiosqlite:///book_shop.db",
    )

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    reg_middlewares(dp, session_maker)
    reg_routes(dp)

    await init_model(engine)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
        print("Бот Запущен!!!")
    except KeyboardInterrupt:
        print("Бот остановлен!")
