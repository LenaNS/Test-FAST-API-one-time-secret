import pytest
import asyncio

from typing import AsyncGenerator
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.database import get_async_session

from src.models import Model
from src.main import app

pytestmark = pytest.mark.asyncio


# Тестовый набор параметров подключения к БД
POSTGRES_USER_TEST = "postgres"
POSTGRES_PASSWORD_TEST = "admin"
POSTGRES_HOST_TEST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB_TEST = "secret_db_test"

# Строка подключения
URL_DATABASE_TEST = f"postgresql+asyncpg://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}@{POSTGRES_HOST_TEST}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}"

async_engine = create_async_engine(URL_DATABASE_TEST)

testing_session_local = async_sessionmaker(async_engine, expire_on_commit=False)

async def override_db() -> AsyncGenerator[AsyncSession, None]:
    async with testing_session_local() as session:
        yield session

app.dependency_overrides[get_async_session] = override_db

@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
