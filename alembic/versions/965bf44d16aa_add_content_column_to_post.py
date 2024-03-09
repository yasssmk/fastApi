"""add Content column to post

Revision ID: 965bf44d16aa
Revises: 496dfa74cdcc
Create Date: 2024-03-09 11:08:48.823457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '965bf44d16aa'
down_revision: Union[str, None] = '496dfa74cdcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("post", "content")
    pass
