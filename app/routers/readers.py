from typing import List
from uuid import UUID

from db import get_db
from fastapi import APIRouter, Body, Depends, HTTPException, status
from schemas.readers import (
    CreateReader,
    ReaderResponse,
    UpdateReader,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils import ListingPagination
from utils.crud import reader

router = APIRouter(prefix="/readers")


@router.get("", summary="Get all Readers", tags=["Listing", "Readers"])
async def get_readers(
    pagination: ListingPagination = Depends(),
    db: AsyncSession = Depends(get_db),
) -> List[ReaderResponse]:
    result = await reader.get_all(db, pagination.skip, pagination.limit)
    return [ReaderResponse.model_validate(publisher) for publisher in result]


@router.get("/{code}", summary="Get specific Publisher", tags=["Detail", "Readers"])
async def get_reader(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> ReaderResponse:
    result = await reader.get(db, code)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reader not found.")

    return ReaderResponse.model_validate(result)


@router.post("", summary="Create new Reader", tags=["Create", "Readers"])
async def create_reader(
    data: CreateReader = Body(),
    db: AsyncSession = Depends(get_db),
) -> ReaderResponse:
    try:
        result = await reader.create(db, data.model_dump())

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error ocured while creating Reader.",
        )

    return ReaderResponse.model_validate(result)


@router.delete("/{code}", summary="Delete specific Reader", tags=["Delete", "Readers"])
async def delete_reader(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> ReaderResponse:
    result = await reader.delete(db, code)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reader not found.")

    return ReaderResponse.model_validate(result)


@router.patch("/{code}", summary="Update specific Reader", tags=["Update", "Readers"])
async def update_reader(
    code: UUID,
    data: UpdateReader = Body(),
    db: AsyncSession = Depends(get_db),
) -> ReaderResponse:
    result = await reader.update(db, code, data.model_dump(exclude_none=True))

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reader not found.")

    return ReaderResponse.model_validate(result)
