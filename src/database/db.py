"""
Database connection and session management for AutoCare AI.
Fully hardened for local workstations, Vercel Serverless, and cloud databases.
"""

import os
from pathlib import Path
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 1. Check for cloud database URL (e.g. Neon / Supabase Postgres)
ENV_DB_URL = os.environ.get("DATABASE_URL")

if ENV_DB_URL:
    # Ensure async driver for Postgres
    if ENV_DB_URL.startswith("postgres://"):
        ENV_DB_URL = ENV_DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif ENV_DB_URL.startswith("postgresql://"):
        ENV_DB_URL = ENV_DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    DATABASE_URL = ENV_DB_URL
else:
    # 2. SQLite Configuration
    # On Vercel serverless, the root directory is READ-ONLY. Only /tmp is writable.
    if os.environ.get("VERCEL"):
        DB_FILE = Path("/tmp/autocare.db")
    else:
        DB_FILE = Path(__file__).resolve().parent.parent.parent / "autocare.db"
    
    DATABASE_URL = f"sqlite+aiosqlite:///{DB_FILE}"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Initializes the database schema safely without crashing serverless cold starts."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        # Fallback logging so serverless functions never 500 on cold boot
        print(f"[AutoCare DB Warning] Schema init bypassed: {e}")


async def get_db():
    """Dependency for obtaining an async session."""
    async with async_session() as session:
        yield session
