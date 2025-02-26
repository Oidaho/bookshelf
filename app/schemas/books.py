from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: Annotated[UUID, Field(...)]
    publisher_code: Annotated[UUID, Field(...)]
    author_code: Annotated[UUID, Field(...)]
    title: Annotated[str, Field(...)]
    publishing_year: Annotated[Optional[int], Field(None, le=10000, ge=0)]
    price: Annotated[float, Field(0.0, ge=0.0)]
    amount: Annotated[int, Field(1, gt=0)]


class CreateBook(BaseModel):
    publisher_code: Annotated[UUID, Field(...)]
    author_code: Annotated[UUID, Field(...)]
    title: Annotated[str, Field(...)]
    publishing_year: Annotated[Optional[int], Field(None, le=10000, ge=0)]
    price: Annotated[float, Field(0.0, ge=0.0)]
    amount: Annotated[int, Field(1, gt=0)]


class UpdateBook(BaseModel):
    publisher_code: Annotated[Optional[UUID], Field(None)]
    author_code: Annotated[Optional[UUID], Field(None)]
    title: Annotated[Optional[str], Field(None)]
    publishing_year: Annotated[Optional[int], Field(None, le=10000, ge=0)]
    price: Annotated[Optional[float], Field(None, ge=0.0)]
    amount: Annotated[Optional[int], Field(None, gt=0)]
