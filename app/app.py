from contextlib import asynccontextmanager

from db import disconnect_db
from fastapi import FastAPI
from routers import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # До загрузки приложения

    yield

    # После выключения
    await disconnect_db()


app = FastAPI(lifespan=lifespan)


app.include_router(v1_router, prefix="/api", tags=["v1"])
