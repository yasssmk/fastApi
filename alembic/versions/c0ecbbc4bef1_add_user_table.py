"""add user table

Revision ID: c0ecbbc4bef1
Revises: f7bdbb844bd6
Create Date: 2024-03-09 11:28:04.990056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0ecbbc4bef1'
down_revision: Union[str, None] = 'f7bdbb844bd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False), sa.Column("email", sa.String(), nullable=False), sa.Column("password", sa.String(), nullable=False), sa.Column("created at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("email"))   
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
