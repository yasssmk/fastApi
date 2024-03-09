"""add other column in posts table

Revision ID: d3f2d85eb2ce
Revises: 851a8fc96f12
Create Date: 2024-03-09 12:08:37.362728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3f2d85eb2ce'
down_revision: Union[str, None] = '851a8fc96f12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "created at")
    op.drop_column("posts", "published")
    pass
