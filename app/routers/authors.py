from typing import List
from uuid import UUID

from crud import author
from db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.authors import (
    Author,
    CreateAuthor,
    UpdateAuthor,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/authors")


@router.get("", summary="Get all Authors", tags=["Listing", "Authors"])
async def get_authors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> List[Author]:
    result = await author.get_all(db, skip, limit)
    return [Author.model_validate(publisher) for publisher in result]


@router.get("/{code}", summary="Get specific Author", tags=["Detail", "Authors"])
async def get_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> Author:
    result = await author.get(db, code)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")

    return Author.model_validate(result)


@router.post("", summary="Create new Author", tags=["Create", "Authors"])
async def create_publisher(
    data: CreateAuthor = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Author:
    try:
        result = await author.create(db, data.model_dump())

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error ocured while creating author.",
        )

    return Author.model_validate(result)


@router.delete("/{code}", summary="Delete specific Author", tags=["Delete", "Authors"])
async def delete_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> Author:
    result = await author.delete(db, code)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found.")

    return Author.model_validate(result)


@router.patch("/{code}", summary="Update specific Author", tags=["Update", "Authors"])
async def update_publisher(
    code: UUID,
    data: UpdateAuthor = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Author:
    result = await author.update(db, code, data.model_dump(exclude_none=True))

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found.")

    return Author.model_validate(result)
