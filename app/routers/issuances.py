from enum import Enum
from typing import List
from uuid import UUID

from db import get_db
from fastapi import APIRouter, Body, Depends
from schemas.issuances import (
    CreateIssuance,
    IssuanceResponse,
    UpdateIssuance,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils import ListingPagination, ListingSort, ListingSearch
from utils.crud import issuance

router = APIRouter(prefix="/issuances")


class SortFields(str, Enum):
    ISSUANCED = "issuanced_at"
    EXPIRES = "expires_at"


class SearchFields(str, Enum):
    ISSUANCED = "issuanced_at"
    EXPIRES = "expires_at"
    READER = "reader_code"
    BOOK = "book_code"


@router.get("", summary="Get all Issuances", tags=["Listing", "Issuances"])
async def get_issuances(
    search: ListingSearch[SearchFields] = Depends(),
    sort: ListingSort[SortFields] = Depends(),
    pagination: ListingPagination = Depends(),
    db: AsyncSession = Depends(get_db),
) -> List[IssuanceResponse]:
    """Возвращает список всех выдач с возможностью поиска, сортировки и пагинации."""
    result = await issuance.get_all(db, search, sort, pagination)
    return [IssuanceResponse.model_validate(publisher) for publisher in result]


@router.get("/{code}", summary="Get specific Issuance", tags=["Detail", "Issuances"])
async def get_issuance(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> IssuanceResponse:
    """Возвращает данные конкретной выдачи по ее коду."""
    result = await issuance.get(db, code)
    return IssuanceResponse.model_validate(result)


@router.post("", summary="Create new Issuance", tags=["Create", "Issuances"])
async def create_issuance(
    data: CreateIssuance = Body(),
    db: AsyncSession = Depends(get_db),
) -> IssuanceResponse:
    """Создает новоую выдачу на основе переданных данных.
    При создании также проверяется существование связанных сущностей.
    Книга не будет выдана, если читатель уже имеет 5 выдач.
    Книга не будет выдана, если их не хватает в библиотеке.
    """
    result = await issuance.create(db, data.model_dump())
    return IssuanceResponse.model_validate(result)


@router.delete("/{code}", summary="Delete specific Issuance", tags=["Delete", "Issuances"])
async def delete_issuance(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> IssuanceResponse:
    """Удаляет конкретную выдачу по ее коду.
    Если при удалении у связанного читателя больше не осталось выдач,
    то он тоже удаляется.
    При удалении книга возвращается 'на полку', т.е. кол-во экземпляров
    книги возрастает на 1.
    """
    result = await issuance.delete(db, code)
    return IssuanceResponse.model_validate(result)


@router.patch("/{code}", summary="Update specific Issuance", tags=["Update", "Issuances"])
async def update_issuance(
    code: UUID,
    data: UpdateIssuance = Body(),
    db: AsyncSession = Depends(get_db),
) -> IssuanceResponse:
    """Обновляет данные конкретной выдачи по ее коду."""
    result = await issuance.update(db, code, data.model_dump(exclude_none=True))
    return IssuanceResponse.model_validate(result)
