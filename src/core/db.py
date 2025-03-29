from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import settings

async_engine = create_async_engine(str(settings.db_dsn_async), echo=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)
