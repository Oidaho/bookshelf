from enum import Enum
from typing import List
from uuid import UUID

from db import get_db
from fastapi import APIRouter, Body, Depends
from schemas.books import (
    BookResponse,
    CreateBook,
    UpdateBook,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils import ListingPagination, ListingSort, ListingSearch
from utils.crud import book

router = APIRouter(prefix="/books")


class SortFields(str, Enum):
    TITLE = "title"
    YEAR = "publishing_year"
    PRICE = "price"
    AMOUNT = "amount"


class SearchFields(str, Enum):
    AUTHOR = "author_code"
    PUBLISHER = "publisher_code"
    YEAR = "publishing_year"
    TITLE = "title"
    PRICE = "price"
    AMOUNT = "amount"


@router.get("", summary="Get all Books", tags=["Listing", "Books"])
async def get_books(
    search: ListingSearch[SearchFields] = Depends(),
    sort: ListingSort[SortFields] = Depends(),
    pagination: ListingPagination = Depends(),
    db: AsyncSession = Depends(get_db),
) -> List[BookResponse]:
    result = await book.get_all(db, search, sort, pagination)
    return [BookResponse.model_validate(publisher) for publisher in result]


@router.get("/{code}", summary="Get specific Book", tags=["Detail", "Books"])
async def get_book(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> BookResponse:
    result = await book.get(db, code)
    return BookResponse.model_validate(result)


@router.post("", summary="Create new Book", tags=["Create", "Books"])
async def create_book(
    data: CreateBook = Body(),
    db: AsyncSession = Depends(get_db),
) -> BookResponse:
    result = await book.create(db, data.model_dump())
    return BookResponse.model_validate(result)


@router.delete("/{code}", summary="Delete specific Book", tags=["Delete", "Books"])
async def delete_book(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> BookResponse:
    result = await book.delete(db, code)
    return BookResponse.model_validate(result)


@router.patch("/{code}", summary="Update specific Book", tags=["Update", "Books"])
async def update_book(
    code: UUID,
    data: UpdateBook = Body(),
    db: AsyncSession = Depends(get_db),
) -> BookResponse:
    result = await book.update(db, code, data.model_dump(exclude_none=True))
    return BookResponse.model_validate(result)
