from sqlalchemy.exc import IntegrityError
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

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.model.__name__} with this data already exists.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error ocured while creating {self.model.__name__}.",
            )

        return db_obj

    async def delete(self, db, code, raise_404=True):
        db_obj = await self.get(db, code, raise_404)

        # Переменные сокращены с целью предотвращения конфликтов имен
        a = await db_obj.awaitable_attrs.author
        p = await db_obj.awaitable_attrs.publisher

        try:
            await db.delete(db_obj)
            await db.commit()

            if len(await a.awaitable_attrs.books) < 1:
                await db.delete(a)
                await db.commit()

            if len(await p.awaitable_attrs.books) < 1:
                await db.delete(p)
                await db.commit()

        # Ошибки целосности отработают на уровне Pyndantic схем
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error ocured while deleting {self.model.__name__}.",
            )
        return db_obj


book = BookCRUD(Book)
