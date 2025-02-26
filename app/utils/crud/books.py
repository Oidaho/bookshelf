from asyncpg.exceptions import UniqueViolationError
from db.models import Book
from fastapi import HTTPException, status

from .authors import author
from .base import CRUD
from .publishers import publisher


class BookCRUD(CRUD[Book]):
    async def create(self, db, obj_in):
        # Переменные сокращены с целью предотвращения конфликтов имен
        a = await author.get(db, code=obj_in.pop("author_code"))
        p = await publisher.get(db, code=obj_in.pop("publisher_code"))

        try:
            db_obj = self.model(**obj_in)
            db_obj.author = a
            db_obj.publisher = p

            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

        except UniqueViolationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.model.__name__} with this data already exists.",
            )

        return db_obj


book = BookCRUD(Book)
