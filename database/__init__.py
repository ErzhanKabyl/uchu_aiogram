from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(
    url="sqlite+aiosqlite:///book_shop.db",
)

session_maker = async_sessionmaker(engine, expire_on_commit=False)