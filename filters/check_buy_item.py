from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from repositories.books import BookRepo
from repositories.user import UserRepo


class FilterUserCanBuyBook(Filter):
    async def __call__(
            self,
            callback: CallbackQuery,
            book_repo: BookRepo,
            user_repo: UserRepo
    ):
        book_id = callback.data.split(":")[-1]
        book = await book_repo.get_book_by_id(book_id)
        user = await user_repo.get_user_by_tg_id(callback.from_user.id)

        if user.balance < book.price:
            await callback.answer(
                "Недостаточно денег!", show_alert=True)
            return

        return True



