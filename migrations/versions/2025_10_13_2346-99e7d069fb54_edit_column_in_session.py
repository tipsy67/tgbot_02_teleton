"""edit column in session

Revision ID: 99e7d069fb54
Revises: d75fb5fc2f25
Create Date: 2025-10-13 23:46:38.592103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99e7d069fb54'
down_revision: Union[str, Sequence[str], None] = 'd75fb5fc2f25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('sessions', sa.Column('phone_number', sa.String(length=12), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('sessions', 'phone_number')
