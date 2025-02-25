from typing import Type, Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

AlchemyModel = TypeVar("AlchemyModel")


class CRUDBase(Generic[AlchemyModel]):
    def __init__(self, model: Type[AlchemyModel]):
        self.model = model

    async def get(self, db: AsyncSession, code: str):
        result = await db.execute(select(self.model).filter(self.model.code == code))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int, limit: int):
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict):
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, code: str):
        db_obj = await self.get(db, code)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj

    async def update(self, db: AsyncSession, code: str, obj_in: dict):
        db_obj = await self.get(db, code)
        if db_obj:
            for field in obj_in:
                setattr(db_obj, field, obj_in[field])
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj
