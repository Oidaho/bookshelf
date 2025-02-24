from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # До загрузки приложения

    yield

    # После выключения


app = FastAPI(lifespan=lifespan)


app.include_router(v1_router, prefix="/api", tags=["v1"])
