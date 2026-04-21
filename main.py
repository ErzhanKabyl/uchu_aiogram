import os
import asyncio
from aiogram import Bot, Dispatcher, Router,types
from aiogram.client import bot
from dotenv import load_dotenv
from handlers import reg_routes
from database.models import BaseModel
from database import engine


load_dotenv()

token = os.getenv('BOT_TOKEN')

async def init_model():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)



async def main():
    bot = Bot(token=token)
    dp = Dispatcher()

    reg_routes(dp)

    await init_model()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
        print("Бот Запущен!!!")
    except KeyboardInterrupt:
        print("Бот остановлен!")
