from aiogram import Dispatcher

from middlewares.session import DataBaseSessionMiddleware


def reg_middlewares(dp:Dispatcher, session_maker):
    dp.update.middleware(DataBaseSessionMiddleware(session_maker))