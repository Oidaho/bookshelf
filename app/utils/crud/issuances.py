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
    """Класс, предоставляющий CRUD операции для сущности Issuance.

    Этот класс наследуется от:
    - `WithParameterizedListing[Issuance]`: Предоставляет функциональность для параметризованного
      получения списка объектов Issuance с поддержкой поиска, сортировки и пагинации.
    - `WithHTTPExceptions[Issuance]`: Добавляет вызов HTTP-исключений при определенных ситуациях,
      которые возникают при исполнении CRUD операций.
    """

    async def create(self, db, obj_in) -> Issuance:
        """Создает сущность и возвращает ее инстанс.
        Дополнительно проверяет существование связанных
        сущностей, а также некоторые условия, связанные с
        существованием достатого кол-ва книг в библиотеке
        для выдачи и допустимым кол-вом этих выдач для
        одного читателя.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            obj_in (dict): Данные для создания сущности.

        Raises:
            HTTPException: 400. Превышено кол-во выдач.
            HTTPException: 400. Не хватает книг.
            HTTPException: 400. Невозможно создать.
            HTTPException: 500. Ошибка при создании.

        Returns:
            Issuance: Созданый инстанс модели Issuance.
        """
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

    async def delete(self, db, code, raise_404=True) -> Issuance:
        """Удаляет сущность и возвращает ее инстанс.
        В случае успешного удаления - возвращает книгу в библиотеку.
        Удаляет читателя, если у него больше нет связанных выдач.
        Вызывает HTTP исключение в случае ошибки удаления.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            code (Union[str, UUID]): UUID (код) сущности.
            raise_404 (bool, optional): Вызывать ли HTTP404 если сущность не найдена. Defaults to True.

        Raises:
            HTTPException: 500. Ошибка при удалении.

        Returns:
            Issuance: Удаленный инстанс модели Issuance.
        """
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
