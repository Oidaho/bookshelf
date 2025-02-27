from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: Annotated[UUID, Field(...)]
    name: Annotated[str, Field(...)]


class CreateAuthor(BaseModel):
    name: Annotated[str, Field(...)]

    @field_validator("name", mode="after")
    @classmethod
    def after_validate_name(cls, name: str) -> str:
        return name.lower().title()


class UpdateAuthor(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
