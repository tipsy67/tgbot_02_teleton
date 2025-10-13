"""edit column in users

Revision ID: 3beb313cad7c
Revises: 6b0db87aed92
Create Date: 2025-10-13 21:05:44.598027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3beb313cad7c'
down_revision: Union[str, Sequence[str], None] = '6b0db87aed92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f('ix_users_tg_id'), table_name='users')
    op.create_index(op.f('ix_users_tg_id'), 'users', ['tg_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_tg_id'), table_name='users')
    op.create_index(op.f('ix_users_tg_id'), 'users', ['tg_id'], unique=True)
