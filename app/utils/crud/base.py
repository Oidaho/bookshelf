from typing import Generic, Type, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

AlchemyModel = TypeVar("AlchemyModel")


class CRUD(Generic[AlchemyModel]):
    def __init__(self, model: Type[AlchemyModel]):
        self.model = model

    async def get_all(self, db: AsyncSession, offset: int, limit: int):
        result = await db.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()

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
