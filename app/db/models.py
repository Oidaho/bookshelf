import uuid

from sqlalchemy import (
    DECIMAL,
    Column,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .engine import BaseORM


class Publisher(BaseORM):
    __tablename__ = "publishers"

    code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    city = Column(String(60), default=None)

    books = relationship("Book", back_populates="publisher")

    __table_args__ = (
        Index("publisher_code_idx", code, postgresql_using="hash"),
        Index("publishers_name_idx", name, postgresql_using="hash"),
    )


class Author(BaseORM):
    __tablename__ = "authors"

    code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, unique=True, nullable=False)

    books = relationship("Book", back_populates="author")

    __table_args__ = (
        Index("author_code_idx", code, postgresql_using="hash"),
        Index("author_name_idx", name, postgresql_using="hash"),
    )


class Book(BaseORM):
    __tablename__ = "books"

    code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publisher_code = Column(UUID(as_uuid=True), ForeignKey("publishers.code"), nullable=False)
    author_code = Column(UUID(as_uuid=True), ForeignKey("authors.code"), nullable=False)
    publishing_year = Column(SmallInteger)
    title = Column(Text)
    price = Column(DECIMAL(10, 2))
    amount = Column(Integer)

    publisher = relationship("Publisher", back_populates="books")
    author = relationship("Author", back_populates="books")

    __table_args__ = (
        Index("books_code_idx", code, postgresql_using="hash"),
        Index("book_title_idx", title, postgresql_using="hash"),
        Index("book_publishing_year_idx", publishing_year),
        Index("book_price_idx", price),
        Index("book_amount_idx", amount),
        CheckConstraint(price > 0, name="check_price_non_negative"),
        CheckConstraint(amount > 0, name="check_amount_non_negative"),
        CheckConstraint(
            (publishing_year > 0) & (publishing_year < 10000), name="check_publishing_year_correct"
        ),
    )


class Reader(BaseORM):
    __tablename__ = "readers"

    code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False, unique=True)

    __table_args__ = (
        Index("reader_code_idx", code, postgresql_using="hash"),
        Index("reader_full_name_idx", full_name, postgresql_using="hash"),
        Index("reader_phone_idx", phone, postgresql_using="hash"),
        CheckConstraint(
            r"phone ~ '^\+\d{1,3}\(\d{1,4}\)\d{3}-\d{2}-\d{2}$'", name="check_phone_format"
        ),
    )
