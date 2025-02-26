from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

PHONE_REGEX = r"^\+\d{1,3}\(\d{1,4}\)\d{3}-\d{2}-\d{2}$"


class ReaderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: Annotated[UUID, Field(...)]
    full_name: Annotated[str, Field(..., max_length=255)]
    phone: Annotated[str, Field(..., pattern=PHONE_REGEX)]
    address: Annotated[Optional[str], Field(None)]


class CreateReader(BaseModel):
    full_name: Annotated[str, Field(..., max_length=255)]
    phone: Annotated[str, Field(..., pattern=PHONE_REGEX)]
    address: Annotated[Optional[str], Field(None)]


class UpdateReader(BaseModel):
    full_name: Annotated[Optional[str], Field(None, max_length=255)]
    phone: Annotated[Optional[str], Field(None, pattern=PHONE_REGEX)]
    address: Annotated[Optional[str], Field(None)]
