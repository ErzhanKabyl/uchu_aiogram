from aiogram import F, Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keybords.catalog import generate_catalog_kb, CategoryCBData, generate_books_kb, BookCBdata, back_to_category_books

catalog_router = Router()

CATALOG = {
    "business": {
        "text": "Бизнес",
        "description": "Книги о бизносе",
        "books": [
            { "id": 1,
              "name": "Книга {}",
              "description": "Описание книги {}",
              "price": 123,
              },
            { "id": 2,
              "name": "Книга {}",
              "description": "Описание книги {}",
              "price": 321,
              },
            { "id": 3,
              "name": "Книга {}",
              "description": "Описание книги {}",
              "price": 213,
              },
        ]
    },
    "programming": {
        "text": "Программирование",
        "description": "Книги о Программирование",
        "books": [
            {"id": 4,
             "name": "Книга {}",
             "description": "Описание книги {}",
             "price": 313,
             },
            {"id": 5,
             "name": "Книга {}",
             "description": "Описание книги {}",
             "price": 10220,
             },
            {"id": 6,
             "name": "Книга {}",
             "description": "Описание книги {}",
             "price": 10022,
             }
        ]
    },
    "detectives": {
        "text": "Детективы",
        "description": "Книги Детективы",
        "books": [
            {"id": 7,
             "name": "Книга {}",
             "description": "Описание книги {}",
             "price": 111100,
             },
            {"id": 8,
             "name": "Книга {}",
             "description": "Описание книги {}",
             "price": 11112200,
             },
            {"id": 9,
             "name": "Книга {}",
             "description": "Описание книги {}",
             "price": 10312310,
             }
        ]
}
}

@catalog_router.callback_query(F.data == "catalog")
@catalog_router.message(F.text == "Каталог")
async def catalog( update: types.Message | types.CallbackQuery ):
    if isinstance(update, types.Message):
        await update.answer(
            "Наш каталог:",
            reply_markup=generate_catalog_kb(CATALOG)
        )
    else:
        await update.message.edit_text(
            "Наш каталог:",
            reply_markup=generate_catalog_kb(CATALOG)
        )


@catalog_router.callback_query(CategoryCBData.filter())
async def category_info(callback:CallbackQuery, callback_data:CategoryCBData):
    category = CATALOG.get(callback_data.category)
    await callback.message.edit_text(
        text=category["description"],
        reply_markup=generate_books_kb(
            category["books"],
            callback_data.category
        )
    )


@catalog_router.callback_query(BookCBdata.filter())
async def book_info(callback:CallbackQuery, callback_data:BookCBdata):
    book_id = callback_data.id
    category = CATALOG.get(callback_data.category)

    book = None

    for bk in category["books"]:
        if bk["id"] == book_id:
            book = bk
            break

    if not book:
        return await callback.answer("Не нашел книгу")

    await callback.message.edit_text(
        f"Название - {book['name'].format(book['id'])}\n"
        f"Описание - {book['description'].format(book['id'])}\n"
        f"Цена - {book['price']}\n\n"
        "Хотите приобрести?",
        reply_markup=back_to_category_books(callback_data.category)
    )
