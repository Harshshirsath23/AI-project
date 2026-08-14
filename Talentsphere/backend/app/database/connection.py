from app.core.config import settings
from app.database.session import (
    sync_engine as engine,
    SyncSessionLocal as SessionLocal,
    get_sync_db as get_db,
    async_engine,
    AsyncSessionLocal,
    get_async_db
)

db_url = settings.sync_database_url

__all__ = ["engine", "SessionLocal", "get_db", "async_engine", "AsyncSessionLocal", "get_async_db", "db_url"]
