from aiogram import Dispatcher
from handlers.start import start_router as start
from handlers.info import info_router as info
from handlers.catalog import catalog_router as catalog


def reg_routes (dp: Dispatcher):
    dp.include_router(start)
    dp.include_router(info)
    dp.include_router(catalog)
