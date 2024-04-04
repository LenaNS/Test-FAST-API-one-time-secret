import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.models import Model

load_dotenv()

# Псевдоимпорт из окружения
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# Строка подключения
URL_DATABASE = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(URL_DATABASE)
session_local = async_sessionmaker(engine, expire_on_commit=False)

# Создание таблиц
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
        
# Удаление таблиц
async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_local() as session:
        yield session