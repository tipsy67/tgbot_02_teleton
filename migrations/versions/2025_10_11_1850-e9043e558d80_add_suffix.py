"""add suffix

Revision ID: e9043e558d80
Revises: 283ce232a2bc
Create Date: 2025-10-11 18:50:01.690918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9043e558d80'
down_revision: Union[str, Sequence[str], None] = '283ce232a2bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('sessions', sa.Column('suffix', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('sessions', 'suffix')
