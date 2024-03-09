"""Fix typo in downgrade function

Revision ID: f7bdbb844bd6
Revises: 965bf44d16aa
Create Date: 2024-03-09 11:23:32.053830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7bdbb844bd6'
down_revision: Union[str, None] = '965bf44d16aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
