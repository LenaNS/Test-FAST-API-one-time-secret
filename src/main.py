from fastapi import FastAPI
from src.router import router

from contextlib import asynccontextmanager
from src.database import create_tables, delete_tables

# Описание сценария ЖЦ приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # print("БД очищена")
    await create_tables()
    print("БД готова к работе")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan) 

app.include_router(router=router)

