"""add column to users

Revision ID: 7ea3f0dc50ec
Revises: 024a07e8f97b
Create Date: 2025-10-13 21:01:37.919190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ea3f0dc50ec'
down_revision: Union[str, Sequence[str], None] = '024a07e8f97b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_active')
