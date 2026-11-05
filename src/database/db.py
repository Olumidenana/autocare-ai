"""
Database connection and session management for AutoCare AI.
"""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent.parent.parent / "autocare.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_FILE}"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Initializes the database schema."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db():
    """Dependency for obtaining an async session."""
    async with async_session() as session:
        yield session
