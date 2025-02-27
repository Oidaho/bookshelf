from pydantic import BaseModel, field_validator
from typing import Annotated, Optional, TypeVar, Generic
from fastapi import Query
from datetime import date
from enum import Enum


class ListingPagination(BaseModel):
    skip: Annotated[int, Query(0, ge=0, example=0)]
    limit: Annotated[int, Query(50, le=200, example=50)]


class ListingFiltering(BaseModel):
    # TODO: write me
    pass


# OrderingFeilds. Имеется в виду Enum
_OF = TypeVar("_OF")


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class ListingSort(BaseModel, Generic[_OF]):
    sort_by: Annotated[Optional[_OF], Query(None, description="Sorting field")]
    sord_order: Annotated[SortOrder, Query(SortOrder.ASC, description="Sorting order")]


class DateSearch(BaseModel):
    date: Annotated[Optional[str], Query(None, example="2025-02-27")]

    @field_validator("date", mode="before")
    @classmethod
    def set_default_date(cls, value: Optional[str]) -> str:
        return value or date.today().isoformat()
