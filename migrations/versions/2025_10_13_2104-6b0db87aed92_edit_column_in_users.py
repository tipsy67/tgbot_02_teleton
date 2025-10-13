"""edit column in users

Revision ID: 6b0db87aed92
Revises: 7ea3f0dc50ec
Create Date: 2025-10-13 21:04:21.672779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b0db87aed92'
down_revision: Union[str, Sequence[str], None] = '7ea3f0dc50ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
