from pydantic import BaseModel, Field
from typing import Annotated
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
    date: Annotated[date, Field(default_factory=date.today)]
