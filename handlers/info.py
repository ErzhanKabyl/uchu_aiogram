from aiogram import Router, types, F

info_router = Router()

@info_router.message(F.text == "О нас")
async def info(message: types.Message):
    await message.answer("Я бот для покупки книг.\n "
                         "У нас много интересного.\n\n"
                         "Хорошего чтения!")