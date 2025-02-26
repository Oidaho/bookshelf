from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: Annotated[UUID, Field(...)]
    name: Annotated[str, Field(...)]


class CreateAuthor(BaseModel):
    name: Annotated[str, Field(...)]


class UpdateAuthor(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
