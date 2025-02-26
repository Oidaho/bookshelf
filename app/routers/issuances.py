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
from utils import ListingPagination
from utils.crud import issuance

router = APIRouter(prefix="/issuances")


@router.get("", summary="Get all Issuances", tags=["Listing", "Issuances"])
async def get_issuances(
    pagination: ListingPagination = Depends(),
    db: AsyncSession = Depends(get_db),
) -> List[IssuanceResponse]:
    result = await issuance.get_all(db, pagination.skip, pagination.limit)
    return [IssuanceResponse.model_validate(publisher) for publisher in result]


@router.get("/{code}", summary="Get specific Issuance", tags=["Detail", "Issuances"])
async def get_issuance(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> IssuanceResponse:
    result = await issuance.get(db, code)
    return IssuanceResponse.model_validate(result)


@router.post("", summary="Create new Issuance", tags=["Create", "Issuances"])
async def create_issuance(
    data: CreateIssuance = Body(),
    db: AsyncSession = Depends(get_db),
) -> IssuanceResponse:
    result = await issuance.create(db, data.model_dump())
    return IssuanceResponse.model_validate(result)


@router.delete("/{code}", summary="Delete specific Issuance", tags=["Delete", "Issuances"])
async def delete_issuance(
    code: UUID,
    db: AsyncSession = Depends(get_db),
) -> IssuanceResponse:
    result = await issuance.delete(db, code)
    return IssuanceResponse.model_validate(result)


@router.patch("/{code}", summary="Update specific Issuance", tags=["Update", "Issuances"])
async def update_issuance(
    code: UUID,
    data: UpdateIssuance = Body(),
    db: AsyncSession = Depends(get_db),
) -> IssuanceResponse:
    result = await issuance.update(db, code, data.model_dump(exclude_none=True))
    return IssuanceResponse.model_validate(result)
