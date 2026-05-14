from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi import Depends
from .config import get_settings
# 1. Define the Database URL

DATABASE_URL=get_settings.DATABASE_URL

if DATABASE_URL is None:
    raise ValueError("Not Found The DataBase URL")

# For async, use asyncpg URL
async_database_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(async_database_url, echo=True)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 
        
        
