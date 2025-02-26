from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional


class ReaderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: UUID
    full_name: str = Field(..., max_length=255)
    address: str = Field(...)
    phone: str = Field(..., pattern=r"^\+\d{1,3}\(\d{1,4}\)\d{3}-\d{2}-\d{2}$")


class CreateReader(BaseModel):
    full_name: str = Field(..., max_length=255)
    address: str = Field(...)
    phone: str = Field(..., pattern=r"^\+\d{1,3}\(\d{1,4}\)\d{3}-\d{2}-\d{2}$")


class UpdateReader(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None)
    phone: Optional[str] = Field(None, pattern=r"^\+\d{1,3}\(\d{1,4}\)\d{3}-\d{2}-\d{2}$")
