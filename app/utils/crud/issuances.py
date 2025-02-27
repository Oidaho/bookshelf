from db.models import Issuance
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from .books import book
from .base import WithHTTPExceptions, WithParameterizedListing
from .readers import reader


# ! Если настолько сложные взаимодействия не будут интересовать в рамках CRUD -
# ! удалите все переопределенные методы и оставьте pass в теле класса.
# ! Также можно откатиться до совсем базовых операций, унаследовав класс
# ! от from .base import BaseCRUD с указанием контекста модели (BaseCRUD[Issuance]).


class IssuanceCRUD(WithParameterizedListing[Issuance], WithHTTPExceptions[Issuance]):
    async def create(self, db, obj_in):
        # * Переменные сокращены с целью предотвращения конфликтов имен
        r = await reader.get(db, code=obj_in.pop("reader_code"))
        b = await book.get(db, code=obj_in.pop("book_code"))

        # * Если читатель уже имеет 5 непогашеных выдач
        if len(await r.awaitable_attrs.issuances) >= 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The number of issuances for this reader has been exceeded.",
            )

        # * Если нехватает книг для выдачи
        if b.amount < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="It is impossible to create issuance. There are not enough books.",
            )
        else:
            # * Забираем книгу "с полки"
            b.amount -= 1

        try:
            # * Создаем выдачу
            db_obj = self.model(**obj_in)
            db_obj.reader = r
            db_obj.book = b

            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

        # * Если такая выдача уже существует
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.model.__name__} with this data already exists.",
            )

        # * Другие ошибки целосности отработают на уровне Pyndantic схем
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error ocured while creating {self.model.__name__}.",
            )

        return db_obj

    async def delete(self, db, code, raise_404=True):
        db_obj = await self.get(db, code, raise_404)

        # * Переменные сокращены с целью предотвращения конфликтов имен
        b = await db_obj.awaitable_attrs.book
        r = await db_obj.awaitable_attrs.reader

        try:
            # * Удаление выдачи
            await db.delete(db_obj)
            await db.commit()

            # * Возврат книги "на полку"
            b.amount += 1

            # * Удаление читателя, если больше нет для него выдач
            if len(await r.awaitable_attrs.issuances) < 1:
                await db.delete(r)
                await db.commit()

        # * Ошибки целосности отработают на уровне Pyndantic схем
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error ocured while deleting {self.model.__name__}.",
            )
        return db_obj


issuance = IssuanceCRUD(Issuance)
