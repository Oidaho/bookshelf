from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional


class PublisherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: UUID
    name: str
    city: Optional[str] = Field(max_length=60)


class CreatePublisher(BaseModel):
    name: str
    city: Optional[str] = Field(default=None, max_length=60)


class UpdatePublisher(BaseModel):
    name: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None, max_length=60)
