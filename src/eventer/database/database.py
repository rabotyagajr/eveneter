from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from eventer.core.config import settings
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from eventer.models.base.base import Base

engine = create_async_engine(url=settings.db_uri, echo=settings.db_echo)

SessionMaker = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно созданы!")


async def get_db() -> AsyncGenerator[AsyncSession, None]:

    async with SessionMaker() as session:
        try:
            yield session
            await session.commit()
        finally:
            await session.close()


DbSession = Annotated[AsyncSession, Depends(get_db)]
