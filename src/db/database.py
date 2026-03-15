from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from src.config import config as c


engine: AsyncEngine = create_async_engine(
    url=f"postgresql+asyncpg://{c.POSTGRES_USER}:{c.POSTGRES_PASSWORD}@{c.POSTGRES_HOST}:{c.POSTGRES_INTERNAL_PORT}/{c.POSTGRES_DB}",
    pool_size=20,
    max_overflow=30
)

new_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
