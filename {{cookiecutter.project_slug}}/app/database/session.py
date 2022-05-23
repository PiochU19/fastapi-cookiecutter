from core import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(settings.database_url)
async_session: AsyncSession = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """Database dependency injection."""
    async with async_session() as session:
        yield session
        await session.commit()
