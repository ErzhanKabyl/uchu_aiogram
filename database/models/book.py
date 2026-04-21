from   database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, foreign
from sqlalchemy import BigInteger, ForeignKey


class Book(BaseModel):
    __tablename__ = 'books'

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name : Mapped[str]
    description : Mapped[str]
    price : Mapped[int]   # 1$ = 100 cent
    category_id : Mapped[int]  = mapped_column(ForeignKey('categories.id'))