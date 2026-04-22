from aiogram import Router, types
from aiogram.filters import Command
from keybords.menu import main_menu_kb
from repositories.user import UserRepo

start_router = Router()

@start_router.message(Command('start'))
async def start_bot (message: types.Message,user_repo: UserRepo):

    await user_repo.create_or_update_user(
        message.from_user.id,
        message.from_user.full_name,
        message.from_user.username
        )

    await message.answer(f"Здравствуйте, {message.from_user.full_name}.\n"
                         f"Добро пожаловать в телеграмм библиотеку.\n"
                          "Выберите нужное снизу!", reply_markup=main_menu_kb())

