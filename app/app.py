from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # До загрузки приложения

    yield

    # После включения


app = FastAPI(lifespan=lifespan)
