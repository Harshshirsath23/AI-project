from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.settings import get_settings
from app.core.logging import get_logger
from app.models.base import Base

logger = get_logger(__name__)

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.database_echo,
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Create sync engine for synchronous API handlers
sync_engine = create_engine(
    settings.sync_database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.database_echo,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()



async def init_db() -> None:
    """Initialize database connection."""
    try:
        async with engine.begin() as conn:
            # Test connection
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error("Failed to establish database connection", error=str(e))
        raise


async def close_db() -> None:
    """Close database connection."""
    await engine.dispose()
    logger.info("Database connection closed")
