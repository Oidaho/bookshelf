from pydantic import BaseModel, field_validator
from typing import Annotated, Optional, TypeVar, Generic, Union
from fastapi import Query
from datetime import date
from enum import Enum


class ListingPagination(BaseModel):
    skip: Annotated[int, Query(0, ge=0, example=0, description="Skipping entries")]
    limit: Annotated[int, Query(50, le=200, example=50, description="Total entries")]


# SearchFields
_SF = TypeVar("_SF", bound=Union[str, Enum])


class SearchMode(str, Enum):
    SIMMILAR = "simmilar"
    EQ = "equal"
    LT = "lower_than"
    GT = "greater_than"


class ListingSearch(BaseModel, Generic[_SF]):
    search_by: Annotated[Optional[_SF], Query(None, description="Search field")]
    search_mode: Annotated[SearchMode, Query(SearchMode.EQ, description="Search Mode")]
    search_value: Annotated[Optional[str], Query(None, description="Search value")]


# OrderingFeilds
_OF = TypeVar("_OF", bound=Union[str, Enum])


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class ListingSort(BaseModel, Generic[_OF]):
    sort_by: Annotated[Optional[_OF], Query(None, description="Sorting field")]
    sort_order: Annotated[SortOrder, Query(SortOrder.ASC, description="Sorting order")]


class DateSearch(BaseModel):
    date: Annotated[Optional[str], Query(None, example="2025-02-27", description="Search date")]

    @field_validator("date", mode="before")
    @classmethod
    def set_default_date(cls, value: Optional[str]) -> str:
        return value or date.today().isoformat()
