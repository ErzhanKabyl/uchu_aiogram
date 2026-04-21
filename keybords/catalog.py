from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


class CategoryCBData(CallbackData, prefix = "category"):
    category: str

class BookCBdata(CallbackData, prefix = "book"):
    id: int
    category: str



def generate_catalog_kb(catalog):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for category_cb, category_name in catalog.items():
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=category_name["text"],
                    callback_data=CategoryCBData(category=category_cb).pack()
                )
            ]
        )

    return keyboard

def generate_books_kb(books, category):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for book in books:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=book["name"].format(book['id']),
                    callback_data=BookCBdata(id = book['id'], category=category).pack()
                )
            ]
        )
    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text="<<< Назад", callback_data="catalog")
        ]
    )

    return keyboard

def back_to_category_books(category):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
            text="<<< Назад",
            callback_data=CategoryCBData(category=category).pack()
        )
        ]
    ]
    )
