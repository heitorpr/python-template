from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import AsyncSessionLocal

"""Dependency for getting a database session."""


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session

            await session.commit()
        except Exception:
            await session.rollback()
            raise
