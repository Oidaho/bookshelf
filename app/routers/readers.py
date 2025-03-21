from enum import Enum
from typing import List
from uuid import UUID

from db import get_db
from fastapi import APIRouter, Body, Depends
from schemas.readers import (
    CreateReader,
    ReaderResponse,
    UpdateReader,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils import ListingPagination, ListingSort, ListingSearch
from utils.crud import reader

router = APIRouter(prefix="/readers")


class SortFields(str, Enum):
    NAME = "full_name"
    ADDRESS = "address"


class SearchFields(str, Enum):
    NAME = "full_name"
    ADDRESS = "address"
    PHONE = "phone"


@router.get("", summary="Get all Readers", tags=["Listing", "Readers"])
async def get_readers(
    search: ListingSearch[SearchFields] = Depends(),
    sort: ListingSort[SortFields] = Depends(),
    pagination: ListingPagination = Depends(),
    db: AsyncSession = Depends(get_db),
) -> List[ReaderResponse]:
    """Возвращает список всех читателей с возможностью поиска, сортировки и пагинации."""
    result = await reader.get_all(db, search, sort, pagination)
    return [ReaderResponse.model_validate(reader) for reader in result]


@router.get("/{code}", summary="Get specific Publisher", tags=["Detail", "Readers"])
async def get_reader(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> ReaderResponse:
    """Возвращает данные конкретного читателя по его коду."""
    result = await reader.get(db, code)
    return ReaderResponse.model_validate(result)


@router.post("", summary="Create new Reader", tags=["Create", "Readers"])
async def create_reader(
    data: CreateReader = Body(),
    db: AsyncSession = Depends(get_db),
) -> ReaderResponse:
    """Создает нового читателя на основе переданных данных."""
    result = await reader.create(db, data.model_dump())
    return ReaderResponse.model_validate(result)


@router.delete("/{code}", summary="Delete specific Reader", tags=["Delete", "Readers"])
async def delete_reader(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> ReaderResponse:
    """Удаляет конкретного читателя по его коду."""
    result = await reader.delete(db, code)
    return ReaderResponse.model_validate(result)


@router.patch("/{code}", summary="Update specific Reader", tags=["Update", "Readers"])
async def update_reader(
    code: UUID,
    data: UpdateReader = Body(),
    db: AsyncSession = Depends(get_db),
) -> ReaderResponse:
    """Обновляет данные конкретного читателя по его коду."""
    result = await reader.update(db, code, data.model_dump(exclude_none=True))
    return ReaderResponse.model_validate(result)
