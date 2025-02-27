from typing import Generic, Optional, Type, TypeVar, Union

from fastapi import HTTPException, status
from sqlalchemy import String, asc, desc, select, Column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..query_params import ListingPagination, ListingSearch, ListingSort, SortOrder

AlchemyModel = TypeVar("AlchemyModel")


class BaseCRUD(Generic[AlchemyModel]):
    def __init__(self, model: Type[AlchemyModel]):
        self.model = model

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def get(self, db: AsyncSession, code: str):
        result = await db.execute(select(self.model).filter(self.model.code == code))
        db_obj = result.scalar_one_or_none()
        return db_obj

    async def create(self, db: AsyncSession, obj_in: dict):
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, code: str):
        db_obj = await self.get(db, code)
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def update(self, db: AsyncSession, code: str, obj_in: dict):
        db_obj = await self.get(db, code)
        for field in obj_in:
            setattr(db_obj, field, obj_in[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class WithHTTPExceptions(BaseCRUD[AlchemyModel]):
    async def get(self, db: AsyncSession, code: str, raise_404: bool = True):
        result = await db.execute(select(self.model).filter(self.model.code == code))
        db_obj = result.scalar_one_or_none()
        if db_obj is None:
            if raise_404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.model.__name__} not found.",
                )
        return db_obj

    async def create(self, db: AsyncSession, obj_in: dict):
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

    async def delete(self, db: AsyncSession, code: str, raise_404: bool = True):
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

    async def update(self, db: AsyncSession, code: str, obj_in: dict, raise_404: bool = True):
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


class WithParameterizedListing(BaseCRUD[AlchemyModel]):
    async def get_all(
        self,
        db: AsyncSession,
        search: Optional[ListingSearch] = None,
        sort: Optional[ListingSort] = None,
        pagination: Optional[ListingPagination] = None,
    ):
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
    def __create_condition(column: Column, operator: str, search_value: Union[str, int, float]):
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

        return column.op(operator)(search_value)
