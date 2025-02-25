import uuid

from sqlalchemy import Column, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID

from .engine import BaseORM


class Publisher(BaseORM):
    __tablename__ = "publishers"

    code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    city = Column(String(60), default=None)

    __table_args__ = (
        Index("publisher_code_idx", code, postgresql_using="hash"),
        Index("publishers_name_idx", name, postgresql_using="hash"),
    )
