from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PublisherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: Annotated[UUID, Field(...)]
    name: Annotated[str, Field(...)]
    city: Annotated[Optional[str], Field(None, max_length=60)]


class CreatePublisher(BaseModel):
    name: Annotated[str, Field(...)]
    city: Annotated[Optional[str], Field(None, max_length=60)]


class UpdatePublisher(BaseModel):
    name: Annotated[Optional[str], Field(None)]
    city: Annotated[Optional[str], Field(None, max_length=60)]
