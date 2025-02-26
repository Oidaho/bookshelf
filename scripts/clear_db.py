import sys
import os

# Разрешение имотра
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from db import get_db
from db.models import *  # noqa
from sqlalchemy import delete
from typing import Collection
import asyncio

models = [Author, Publisher, Reader, Book, Issuance]


async def clear_tables(obj_collection: Collection):
    async for session in get_db():
        for model in obj_collection:
            await session.execute(delete(model))
            await session.commit()


async def main():
    await clear_tables(models)


if __name__ == "__main__":
    asyncio.run(main())
