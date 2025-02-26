from typing import List
from uuid import UUID

from db import get_db
from fastapi import APIRouter, Body, Depends
from schemas.authors import (
    AuthorResponse,
    CreateAuthor,
    UpdateAuthor,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils import ListingPagination
from utils.crud import author

router = APIRouter(prefix="/authors")


@router.get("", summary="Get all Authors", tags=["Listing", "Authors"])
async def get_authors(
    pagination: ListingPagination = Depends(),
    db: AsyncSession = Depends(get_db),
) -> List[AuthorResponse]:
    result = await author.get_all(db, pagination.skip, pagination.limit)
    return [AuthorResponse.model_validate(author) for author in result]


@router.get("/{code}", summary="Get specific Author", tags=["Detail", "Authors"])
async def get_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> AuthorResponse:
    result = await author.get(db, code)
    return AuthorResponse.model_validate(result)


@router.post("", summary="Create new Author", tags=["Create", "Authors"])
async def create_publisher(
    data: CreateAuthor = Body(),
    db: AsyncSession = Depends(get_db),
) -> AuthorResponse:
    result = await author.create(db, data.model_dump())
    return AuthorResponse.model_validate(result)


@router.delete("/{code}", summary="Delete specific Author", tags=["Delete", "Authors"])
async def delete_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> AuthorResponse:
    result = await author.delete(db, code)
    return AuthorResponse.model_validate(result)


@router.patch("/{code}", summary="Update specific Author", tags=["Update", "Authors"])
async def update_publisher(
    code: UUID,
    data: UpdateAuthor = Body(),
    db: AsyncSession = Depends(get_db),
) -> AuthorResponse:
    result = await author.update(db, code, data.model_dump(exclude_none=True))
    return AuthorResponse.model_validate(result)
