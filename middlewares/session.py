from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message

from repositories.books import BookRepo
from repositories.categories import CategoryRepo
from repositories.user import UserRepo


class DataBaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker) -> None:
        self.session_maker = session_maker

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_maker() as session:
            data['user_repo'] = UserRepo(session=session)
            data['category_repo'] = CategoryRepo(session=session)
            data['book_repo'] = BookRepo(session=session)
            return await handler(event, data)