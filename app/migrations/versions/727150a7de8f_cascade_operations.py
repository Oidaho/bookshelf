"""Cascade operations

Revision ID: 727150a7de8f
Revises: be154ca65300
Create Date: 2025-02-25 20:00:15.374957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '727150a7de8f'
down_revision: Union[str, None] = 'be154ca65300'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('books_author_code_fkey', 'books', type_='foreignkey')
    op.drop_constraint('books_publisher_code_fkey', 'books', type_='foreignkey')
    op.create_foreign_key(None, 'books', 'authors', ['author_code'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'books', 'publishers', ['publisher_code'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('issuances_reader_code_fkey', 'issuances', type_='foreignkey')
    op.drop_constraint('issuances_book_code_fkey', 'issuances', type_='foreignkey')
    op.create_foreign_key(None, 'issuances', 'books', ['book_code'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'issuances', 'readers', ['reader_code'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'issuances', type_='foreignkey')
    op.drop_constraint(None, 'issuances', type_='foreignkey')
    op.create_foreign_key('issuances_book_code_fkey', 'issuances', 'books', ['book_code'], ['code'])
    op.create_foreign_key('issuances_reader_code_fkey', 'issuances', 'readers', ['reader_code'], ['code'])
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.create_foreign_key('books_publisher_code_fkey', 'books', 'publishers', ['publisher_code'], ['code'])
    op.create_foreign_key('books_author_code_fkey', 'books', 'authors', ['author_code'], ['code'])
    # ### end Alembic commands ###
