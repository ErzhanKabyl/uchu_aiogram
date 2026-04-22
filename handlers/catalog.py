from aiogram import F, Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keybords.catalog import generate_catalog_kb, CategoryCBData, generate_books_kb, BookCBdata, back_to_category_books
from repositories.books import BookRepo
from repositories.categories import CategoryRepo
catalog_router = Router()


@catalog_router.callback_query(F.data == "catalog")
@catalog_router.message(F.text == "Каталог")
async def catalog( update: types.Message | types.CallbackQuery, category_repo: CategoryRepo):

    categories = await category_repo.get_list()

    if isinstance(update, types.Message):
        await update.answer(
            "Наш каталог:",
            reply_markup=generate_catalog_kb(categories)
        )
    else:
        await update.message.edit_text(
            "Наш каталог:",
            reply_markup=generate_catalog_kb(categories)
        )


@catalog_router.callback_query(CategoryCBData.filter())
async def category_info(
        callback:CallbackQuery,
        callback_data:CategoryCBData,
        category_repo: CategoryRepo,
        book_repo: BookRepo,
                 ):
    category = await category_repo.get_by_id(callback_data.category_id)
    books = await book_repo.get_books_by_category_id(callback_data.category_id)

    await callback.message.edit_text(
        text=category.description,
        reply_markup=generate_books_kb(books)
    )


@catalog_router.callback_query(BookCBdata.filter())
async def book_info(
        callback:CallbackQuery,
        callback_data:BookCBdata,
        book_repo:BookRepo
):
    book = await book_repo.get_book_by_id(callback_data.id)




    if not book:
        return await callback.answer("Не нашел книгу")

    await callback.message.edit_text(
        f"Название - {book.name}\n "
        f"Описание - {book.description}\n" 
        f"Цена - {book.price} тг.\n\n"
        "Хотите приобрести?",
        reply_markup=back_to_category_books(book.id, book.category_id)
    )
