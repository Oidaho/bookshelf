from typing import List
from uuid import UUID

from db import get_db
from fastapi import APIRouter, Body, Depends
from schemas.publishers import (
    CreatePublisher,
    PublisherResponse,
    UpdatePublisher,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils import ListingPagination
from utils.crud import publisher

router = APIRouter(prefix="/publishers")


@router.get("", summary="Get all Publishers", tags=["Listing", "Publishers"])
async def get_publishers(
    pagination: ListingPagination = Depends(),
    db: AsyncSession = Depends(get_db),
) -> List[PublisherResponse]:
    result = await publisher.get_all(db, pagination.skip, pagination.limit)
    return [PublisherResponse.model_validate(publisher) for publisher in result]


@router.get("/{code}", summary="Get specific Publisher", tags=["Detail", "Publishers"])
async def get_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> PublisherResponse:
    result = await publisher.get(db, code)
    return PublisherResponse.model_validate(result)


@router.post("", summary="Create new Publisher", tags=["Create", "Publishers"])
async def create_publisher(
    data: CreatePublisher = Body(),
    db: AsyncSession = Depends(get_db),
) -> PublisherResponse:
    result = await publisher.create(db, data.model_dump())
    return PublisherResponse.model_validate(result)


@router.delete("/{code}", summary="Delete specific Publisher", tags=["Delete", "Publishers"])
async def delete_publisher(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> PublisherResponse:
    result = await publisher.delete(db, code)
    return PublisherResponse.model_validate(result)


@router.patch("/{code}", summary="Update specific Publisher", tags=["Update", "Publishers"])
async def update_publisher(
    code: UUID,
    data: UpdatePublisher = Body(),
    db: AsyncSession = Depends(get_db),
) -> PublisherResponse:
    result = await publisher.update(db, code, data.model_dump(exclude_none=True))
    return PublisherResponse.model_validate(result)
