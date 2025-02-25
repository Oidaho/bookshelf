from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional


class Author(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: UUID
    name: str


class CreateAuthor(BaseModel):
    name: str


class UpdateAuthor(BaseModel):
    name: Optional[str] = Field(default=None)
