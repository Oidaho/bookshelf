from db.models import Book
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from .authors import author
from .base import WithHTTPExceptions, WithParameterizedListing
from .publishers import publisher

# ! Если настолько сложные взаимодействия не будут интересовать в рамках CRUD -
# ! удалите все переопределенные методы и оставьте pass в теле класса.
# ! Также можно откатиться до совсем базовых операций, унаследовав класс
# ! от from .base import BaseCRUD с указанием контекста модели (BaseCRUD[Issuance]).


class BookCRUD(WithParameterizedListing[Book], WithHTTPExceptions[Book]):
    """Класс, предоставляющий CRUD операции для сущности Book.

    Этот класс наследуется от:
    - `WithParameterizedListing[Book]`: Предоставляет функциональность для параметризованного
      получения списка объектов Book с поддержкой поиска, сортировки и пагинации.
    - `WithHTTPExceptions[Book]`: Добавляет вызов HTTP-исключений при определенных ситуациях,
      которые возникают при исполнении CRUD операций.
    """

    async def create(self, db, obj_in):
        """Создает сущность и возвращает ее инстанс.
        Проверяет существование связонных сущностей.
        Вызывает HTTP исключения в случае невозможности или
        ошибки создания.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            obj_in (dict): Данные для создания сущности.

        Raises:
            HTTPException: 400. Невозможно создать.
            HTTPException: 500. Ошибка при создании.

        Returns:
            Book: Созданый инстанс модели Book.
        """
        # * Переменные сокращены с целью предотвращения конфликтов имен
        a = await author.get(db, code=obj_in.pop("author_code"))
        p = await publisher.get(db, code=obj_in.pop("publisher_code"))

        try:
            # * Создаем книгу
            db_obj = self.model(**obj_in)
            db_obj.author = a
            db_obj.publisher = p

            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

        # * Если такая книга уже существует
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

    async def delete(self, db, code, raise_404=True) -> Book:
        """Удаляет сущность и возвращает ее инстанс.
        Также удаляет связанного автора и издателя, если у
        тех не осталось связанных книг.
        Вызывает HTTP исключение в случае ошибки удаления.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            code (Union[str, UUID]): UUID (код) сущности.
            raise_404 (bool, optional): Вызывать ли HTTP404 если сущность не найдена. Defaults to True.

        Raises:
            HTTPException: 500. Ошибка при удалении.

        Returns:
            Book: Удаленный инстанс модели Book.
        """
        db_obj = await self.get(db, code, raise_404)

        # * Переменные сокращены с целью предотвращения конфликтов имен
        a = await db_obj.awaitable_attrs.author
        p = await db_obj.awaitable_attrs.publisher

        try:
            # * Удаление книги
            await db.delete(db_obj)
            await db.commit()

            # * Если у связанного автора больше нет книг
            if len(await a.awaitable_attrs.books) < 1:
                await db.delete(a)
                await db.commit()

            # * Если у связанного издательства больше нет книг
            if len(await p.awaitable_attrs.books) < 1:
                await db.delete(p)
                await db.commit()

        # * Ошибки целосности отработают на уровне Pyndantic схем
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error ocured while deleting {self.model.__name__}.",
            )
        return db_obj


book = BookCRUD(Book)
