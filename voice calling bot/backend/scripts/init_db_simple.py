"""
Simple database initialization script without Alembic.

This script:
1. Creates the database if it doesn't exist
2. Creates all tables directly using SQLAlchemy
3. Simpler and more reliable than Alembic for initial setup

Usage:
    python scripts/init_db_simple.py
"""

import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Set Windows event loop policy before importing async libraries
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import get_settings
from app.database.connection import Base


async def create_database_if_not_exists(settings) -> None:
    """
    Create the database if it doesn't exist.
    
    Args:
        settings: Application settings
    """
    # Use 127.0.0.1 instead of localhost to avoid DNS resolution issues
    host = "127.0.0.1" if settings.db_host == "localhost" else settings.db_host
    
    # Connect to PostgreSQL default database (postgres)
    conn = await asyncpg.connect(
        host=host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database="postgres",
    )
    
    try:
        # Check if database exists
        db_exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            settings.db_name
        )
        
        if db_exists:
            print(f"Database '{settings.db_name}' already exists.")
        else:
            # Create database
            await conn.execute(
                f'CREATE DATABASE "{settings.db_name}"'
            )
            print(f"Database '{settings.db_name}' created successfully.")
    
    finally:
        await conn.close()


async def create_tables(settings) -> None:
    """
    Create all tables using SQLAlchemy async engine with asyncpg.
    
    Args:
        settings: Application settings
    """
    # Use async database URL (asyncpg) - works on Windows
    engine = create_async_engine(settings.database_url)
    
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")
    
    await engine.dispose()


async def main():
    """Main entry point."""
    settings = get_settings()
    
    print(f"Database Host: {settings.db_host}")
    print(f"Database Port: {settings.db_port}")
    print(f"Database Name: {settings.db_name}")
    print(f"Database User: {settings.db_user}")
    print(f"Database URL: {settings.database_url}")
    print("-" * 50)
    
    try:
        # Create database if it doesn't exist
        await create_database_if_not_exists(settings)
        
        # Create all tables
        await create_tables(settings)
        
        print("Database initialization completed successfully.")
    
    except Exception as e:
        print(f"Error during database initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
