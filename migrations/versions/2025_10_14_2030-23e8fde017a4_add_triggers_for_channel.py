"""add triggers for channel

Revision ID: 23e8fde017a4
Revises: 59478ab48a4d
Create Date: 2025-10-14 20:30:48.267642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23e8fde017a4'
down_revision: Union[str, Sequence[str], None] = '59478ab48a4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('channels', sa.Column('triggers', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('channels', 'triggers')
