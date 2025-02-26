from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class IssuanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: Annotated[UUID, Field(...)]
    book_code: Annotated[UUID, Field(...)]
    reader_code: Annotated[UUID, Field(...)]
    issuanced_at: Annotated[date, Field(...)]
    expires_at: Annotated[date, Field(...)]


class CreateIssuance(BaseModel):
    book_code: Annotated[UUID, Field(...)]
    reader_code: Annotated[UUID, Field(...)]


class UpdateIssuance(BaseModel):
    book_code: Annotated[Optional[UUID], Field(None)]
    reader_code: Annotated[Optional[UUID], Field(None)]
    issuanced_at: Annotated[Optional[date], Field(None)]
    expires_at: Annotated[Optional[date], Field(None)]
