from typing import List
from uuid import UUID

from crud import publisher
from db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.publishers import (
    Publisher,
    CreatePublisher,
    UpdatePublisher,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/publishers")


@router.get("", summary="Get all Publishers", tags=["Listing", "Publishers"])
async def get_publishers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> List[Publisher]:
    result = await publisher.get_all(db, skip, limit)
    return [Publisher.model_validate(publisher) for publisher in result]


@router.get("/{code}", summary="Get specific Publisher", tags=["Detail", "Publishers"])
async def get_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> Publisher:
    result = await publisher.get(db, code)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found.")

    return Publisher.model_validate(result)


@router.post("", summary="Create new Publisher", tags=["Create", "Publishers"])
async def create_publisher(
    data: CreatePublisher = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Publisher:
    try:
        result = await publisher.create(db, data.model_dump())

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error ocured while creating publisher.",
        )

    return Publisher.model_validate(result)


@router.delete("/{code}", summary="Delete specific Publisher", tags=["Delete", "Publishers"])
async def delete_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> Publisher:
    result = await publisher.delete(db, code)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found.")

    return Publisher.model_validate(result)


@router.patch("/{code}", summary="Update specific Publisher", tags=["Update", "Publishers"])
async def update_publisher(
    code: UUID,
    data: UpdatePublisher = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Publisher:
    result = await publisher.update(db, code, data.model_dump(exclude_none=True))

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found.")

    return Publisher.model_validate(result)
