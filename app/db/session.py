from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import get_settings

settings = get_settings()

echo_sql = settings.debug
engine = create_async_engine(settings.database_url, echo=echo_sql, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:  # type: ignore
        yield session
