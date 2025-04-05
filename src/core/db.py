from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import settings

async_engine = create_async_engine(
    str(settings.db_dsn_async),
    echo=settings.debug,
    pool_size=settings.db_pool_size,  # number of connections to keep in the pool
    max_overflow=0,  # no overflow connections
    pool_timeout=30,  # will wait for 30 seconds before giving up on getting a connection
    pool_recycle=1800,  # will recycle connections after 30 minutes
    pool_pre_ping=True,  # ensure the connection is alive before using it
)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)
