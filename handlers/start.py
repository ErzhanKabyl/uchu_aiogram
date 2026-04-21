from aiogram import Router, types
from aiogram.filters import Command
from keybords.menu import main_menu_kb


start_router = Router()

@start_router.message(Command('start'))
async def start_bot (message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}.\n"
                         f"Добро пожаловать в телеграмм библиотеку.\n"
                          "Выберите нужное снизу!", reply_markup=main_menu_kb())

