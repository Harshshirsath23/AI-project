"""
Database initialization script.

This script:
1. Creates the database if it doesn't exist
2. Runs Alembic migrations to create/update tables
3. Can be used to reset the database if needed

Usage:
    python scripts/init_db.py              # Initialize database
    python scripts/init_db.py --reset      # Reset database (drop and recreate)
    python scripts/init_db.py --migrate    # Only run migrations
"""

import asyncio
import argparse
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
from alembic.config import Config
from alembic import command

from app.config.settings import get_settings


async def create_database_if_not_exists(settings) -> None:
    """
    Create the database if it doesn't exist.
    
    Args:
        settings: Application settings
    """
    # Connect to PostgreSQL default database (postgres)
    conn = await asyncpg.connect(
        host=settings.db_host,
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


async def drop_database_if_exists(settings) -> None:
    """
    Drop the database if it exists.
    
    Args:
        settings: Application settings
    """
    # Connect to PostgreSQL default database (postgres)
    conn = await asyncpg.connect(
        host=settings.db_host,
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
            # Terminate all connections to the database
            await conn.execute(
                f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{settings.db_name}'
                AND pid <> pg_backend_pid()
                """
            )
            
            # Drop database
            await conn.execute(
                f'DROP DATABASE "{settings.db_name}"'
            )
            print(f"Database '{settings.db_name}' dropped successfully.")
        else:
            print(f"Database '{settings.db_name}' does not exist.")
    
    finally:
        await conn.close()


def run_migrations(settings) -> None:
    """
    Run Alembic migrations to create/update tables.
    
    Args:
        settings: Application settings
    """
    alembic_ini = Path(__file__).parent.parent / "alembic.ini"
    
    config = Config(str(alembic_ini))
    # Use sync database URL for migrations (psycopg3 in sync mode)
    config.set_main_option("sqlalchemy.url", settings.sync_database_url)
    
    # Upgrade to latest migration
    print("Running database migrations...")
    command.upgrade(config, "head")
    print("Database migrations completed successfully.")


def reset_migrations(settings) -> None:
    """
    Reset Alembic migrations (downgrade to base, then upgrade).
    
    Args:
        settings: Application settings
    """
    alembic_ini = Path(__file__).parent.parent / "alembic.ini"
    
    config = Config(str(alembic_ini))
    # Use sync database URL for migrations (psycopg3 in sync mode)
    config.set_main_option("sqlalchemy.url", settings.sync_database_url)
    
    # Downgrade to base
    print("Downgrading database to base...")
    command.downgrade(config, "base")
    
    # Upgrade to latest
    print("Upgrading database to latest...")
    command.upgrade(config, "head")
    
    print("Database migrations reset successfully.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Database initialization script")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset database (drop and recreate)"
    )
    parser.add_argument(
        "--migrate-only",
        action="store_true",
        help="Only run migrations, don't create database"
    )
    parser.add_argument(
        "--reset-migrations",
        action="store_true",
        help="Reset migrations (downgrade to base, then upgrade)"
    )
    
    args = parser.parse_args()
    
    settings = get_settings()
    
    print(f"Database Host: {settings.db_host}")
    print(f"Database Port: {settings.db_port}")
    print(f"Database Name: {settings.db_name}")
    print(f"Database User: {settings.db_user}")
    print("-" * 50)
    
    try:
        if args.reset:
            # Reset database
            print("Resetting database...")
            asyncio.run(drop_database_if_exists(settings))
            asyncio.run(create_database_if_not_exists(settings))
            run_migrations(settings)
            print("Database reset completed successfully.")
        
        elif args.migrate_only:
            # Only run migrations
            if args.reset_migrations:
                reset_migrations(settings)
            else:
                run_migrations(settings)
        
        else:
            # Normal initialization
            asyncio.run(create_database_if_not_exists(settings))
            run_migrations(settings)
            print("Database initialization completed successfully.")
    
    except Exception as e:
        print(f"Error during database initialization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
