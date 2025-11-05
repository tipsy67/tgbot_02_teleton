"""add is_active column

Revision ID: 45832b012f69
Revises: 23e8fde017a4
Create Date: 2025-11-05 23:04:59.610834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45832b012f69'
down_revision: Union[str, Sequence[str], None] = '23e8fde017a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('channels', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.execute("UPDATE channels SET is_active = true")
    op.alter_column('channels', 'is_active', nullable=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('channels', 'is_active')
