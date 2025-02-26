from typing import List
from uuid import UUID

from db import get_db
from fastapi import APIRouter, Body, Depends, HTTPException, status
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

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")

    return AuthorResponse.model_validate(result)


@router.post("", summary="Create new Author", tags=["Create", "Authors"])
async def create_publisher(
    data: CreateAuthor = Body(),
    db: AsyncSession = Depends(get_db),
) -> AuthorResponse:
    try:
        result = await author.create(db, data.model_dump())

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error ocured while creating author.",
        )

    return AuthorResponse.model_validate(result)


@router.delete("/{code}", summary="Delete specific Author", tags=["Delete", "Authors"])
async def delete_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> AuthorResponse:
    result = await author.delete(db, code)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found.")

    return AuthorResponse.model_validate(result)


@router.patch("/{code}", summary="Update specific Author", tags=["Update", "Authors"])
async def update_publisher(
    code: UUID,
    data: UpdateAuthor = Body(),
    db: AsyncSession = Depends(get_db),
) -> AuthorResponse:
    result = await author.update(db, code, data.model_dump(exclude_none=True))

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found.")

    return AuthorResponse.model_validate(result)
