from functools import wraps

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


DATABSE_URL = settings.DATABASE_URL


engine = create_async_engine(DATABSE_URL, echo=True)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


def connection(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        async with async_session_maker() as session:
            return await method(self, session, *args, **kwargs)

    return wrapper
