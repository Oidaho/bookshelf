"""book title not uniq

Revision ID: 52b046c68e63
Revises: 3891e8e1f43b
Create Date: 2025-02-26 19:44:47.621367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52b046c68e63'
down_revision: Union[str, None] = '3891e8e1f43b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('books_title_key', 'books', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('books_title_key', 'books', ['title'])
    # ### end Alembic commands ###
