from db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils import DateSearch

router = APIRouter(prefix="/reports")


@router.get("", summary="Get a library report", tags=["Reports"])
async def get_readers(
    search: DateSearch = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return search.date
