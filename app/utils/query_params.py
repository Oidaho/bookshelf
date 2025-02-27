from pydantic import BaseModel, field_validator
from typing import Annotated, Optional
from fastapi import Query
from datetime import date


class ListingPagination(BaseModel):
    skip: Annotated[int, Query(0, ge=0, example=0)]
    limit: Annotated[int, Query(50, le=200, example=50)]


class ListingFiltering(BaseModel):
    # TODO: write me
    pass


class ListingOrdering(BaseModel):
    # TODO: write me
    pass


class DateSearch(BaseModel):
    date: Annotated[Optional[str], Query(None, example="2025-02-27")]

    @field_validator("date", mode="before")
    @classmethod
    def set_default_date(cls, value: Optional[str]) -> str:
        return value or date.today().isoformat()
