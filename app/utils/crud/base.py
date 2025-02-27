from datetime import date
from typing import Generic, Optional, Protocol, Type, TypeVar, Union, List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Column, String, asc, desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..query_params import ListingPagination, ListingSearch, ListingSort, SortOrder


class Codable(Protocol):
    """Протокол, описывающий обьект,
    который имеет в своей сигнатуре колонку code типа UUID.
    """

    code: Column[UUID]


# AlchemyModel
_AM = TypeVar("_AM", bound=Codable)


class BaseCRUD(Generic[_AM]):
    """Базовый класс для реализации операций CRUD для моделей SQLAlchemy,
    которые имеют поле code (UUID) в качестве свеого PrimaryKey.
    """

    def __init__(self, model: Type[_AM]):
        self.model = model

    async def get_all(self, db: AsyncSession) -> List[_AM]:
        """Возвращает листинг сущностей в БД.

        Args:
            db (AsyncSession): Асинхронная сессия БД.

        Returns:
            List[_AM]: Список инстансов моделей SLQAlchemy.
        """
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def get(self, db: AsyncSession, code: Union[str, UUID]) -> _AM:
        """Возвращает сущность по ее коду (code).

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            code (Union[str, UUID]): UUID (код) сущности.

        Returns:
            _AM: Инстанс модели SLQAlchemy.
        """
        result = await db.execute(select(self.model).filter(self.model.code == code))
        db_obj = result.scalar_one_or_none()
        return db_obj

    async def create(self, db: AsyncSession, obj_in: dict) -> _AM:
        """Создает сущность и возвращает ее инстанс.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            obj_in (dict): Данные для создания сущности.

        Returns:
            _AM: Созданый инстанс модели SLQAlchemy.
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, code: Union[str, UUID]) -> _AM:
        """Удаляет сущность и возвращает ее инстанс.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            code (Union[str, UUID]): Код сущности.

        Returns:
            _AM: Удаленный инстанс модели SLQAlchemy.
        """
        db_obj = await self.get(db, code)
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def update(self, db: AsyncSession, code: Union[str, UUID], obj_in: dict) -> _AM:
        """Обновляет сущность и возвращает ее измененный инстанс.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            obj_in (dict): Данные для обновления полей сущности.

        Returns:
            _AM: Измененный инстанс модели SLQAlchemy.
        """
        db_obj = await self.get(db, code)
        for field in obj_in:
            setattr(db_obj, field, obj_in[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class WithHTTPExceptions(BaseCRUD[_AM]):
    """Класс предоставляет переопределенную функции CRUD операций,
    имеющую дополнительные вызовы HTTP исключений в определенных ситуациях,
    в отличие от базовго CRUD класса.
    """

    async def get(
        self,
        db: AsyncSession,
        code: Union[str, UUID],
        raise_404: bool = True,
    ) -> _AM:
        """Возвращает сущность по ее коду (code).
        вызывает HTTP исключение в случае ее отсутствия.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            code (Union[str, UUID]): UUID (код) сущности.
            raise_404 (bool, optional): Вызывать ли HTTP404 если сущность не найдена. Defaults to True.

        Raises:
            HTTPException: 404. Сущность отсутствует в БД.

        Returns:
            _AM: Инстанс модели SLQAlchemy.
        """
        result = await db.execute(select(self.model).filter(self.model.code == code))
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            if raise_404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.model.__name__} not found.",
                )
        return db_obj

    async def create(
        self,
        db: AsyncSession,
        obj_in: dict,
    ) -> _AM:
        """Создает сущность и возвращает ее инстанс.
        Вызывает HTTP исключения в случае невозможности или
        ошибки создания.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            obj_in (dict): Данные для создания сущности.

        Raises:
            HTTPException: 400. Невозможно создать.
            HTTPException: 500. Ошибка при создании.

        Returns:
            _AM: Созданый инстанс модели SLQAlchemy.
        """
        try:
            db_obj = self.model(**obj_in)
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

    async def delete(
        self,
        db: AsyncSession,
        code: Union[str, UUID],
        raise_404: bool = True,
    ) -> _AM:
        """Удаляет сущность и возвращает ее инстанс.
        Вызывает HTTP исключение в случае ошибки удаления.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            code (Union[str, UUID]): UUID (код) сущности.
            raise_404 (bool, optional): Вызывать ли HTTP404 если сущность не найдена. Defaults to True.

        Raises:
            HTTPException: 500. Ошибка при удалении.

        Returns:
            _AM: Удаленный инстанс модели SLQAlchemy.
        """
        db_obj = await self.get(db, code, raise_404)
        try:
            await db.delete(db_obj)
            await db.commit()

        # Ошибки целосности отработают на уровне Pyndantic схем
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error ocured while deleting {self.model.__name__}.",
            )
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        code: Union[str, UUID],
        obj_in: dict,
        raise_404: bool = True,
    ) -> _AM:
        """Обновляет сущность и возвращает ее измененный инстанс.
        Вызывает HTTP исключение при ошибке обнолвения данных.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            code (Union[str, UUID]): UUID (код) сущности.
            obj_in (dict): Данные для обновления полей сущности.
            raise_404 (bool, optional): Вызывать ли HTTP404 если сущность не найдена. Defaults to True.

        Raises:
            HTTPException: 500. Ошибка при обновлении данных.

        Returns:
            _AM: Измененный инстанс модели SLQAlchemy.
        """
        db_obj = await self.get(db, code, raise_404)
        try:
            for field in obj_in:
                setattr(db_obj, field, obj_in[field])
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

        # Ошибки целосности отработают на уровне Pyndantic схем
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error ocured while updating {self.model.__name__}.",
            )
        return db_obj


class WithParameterizedListing(BaseCRUD[_AM]):
    """Класс предоставляет переопределенную функцию листинга,
    имеющую дополнительные параметры сортировки, поиска и пагинации,
    в отличие от базовго CRUD класса.
    """

    async def get_all(
        self,
        db: AsyncSession,
        search: Optional[ListingSearch] = None,
        sort: Optional[ListingSort] = None,
        pagination: Optional[ListingPagination] = None,
    ) -> List[_AM]:
        """Возвращает листинг сущностей в БД, с примененным к нему
        поиску, сортировке и пагинации.

        Args:
            db (AsyncSession): Асинхронная сессия БД.
            search (Optional[ListingSearch], optional): Данные для поиска. Defaults to None.
            sort (Optional[ListingSort], optional): Данные для сортировки. Defaults to None.
            pagination (Optional[ListingPagination], optional): Данные для пагинации. Defaults to None.

        Returns:
            List[_AM]: Список инстансов моделей SLQAlchemy.
        """
        query = select(self.model)

        # Если задан поиск по полю
        if search and search.search_by:
            column = getattr(self.model, search.search_by)
            opreator = search.search_mode.get_operator()
            condition = self.__create_condition(
                column=column,
                operator=opreator,
                search_value=search.search_value,
            )
            query = query.where(condition)

        # Если задана сортировка по полю
        if sort and sort.sort_by:
            ordering = (
                desc(sort.sort_by) if sort.sort_order == SortOrder.DESC else asc(sort.sort_by)
            )
            query = query.order_by(ordering)

        # Если задана пагинация
        if pagination:
            query = query.offset(pagination.skip).limit(pagination.limit)

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    def __create_condition(
        column: Column, operator: str, search_value: Union[str, int, float, date]
    ):
        if operator == "ILIKE":
            if not isinstance(column.type, String):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot use this search mode on non-string field",
                )
            return getattr(column, operator.lower())(f"%{search_value}%")

        elif operator != "=" and isinstance(column.type, String):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot use this search mode on non-numeric field",
            )

        elif operator in ("<", ">", "<=", ">=") and isinstance(search_value, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot use this search mode with non-numeric or non-date search value",
            )

        return column.op(operator)(search_value)
