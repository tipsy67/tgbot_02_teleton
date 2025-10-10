"""initial

Revision ID: 89a7722c9d98
Revises: 
Create Date: 2025-10-10 22:39:54.536271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89a7722c9d98'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('sessions',
    sa.Column('api_id', sa.Integer(), nullable=False),
    sa.Column('session_string', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sessions')),
    sa.UniqueConstraint('api_id', name=op.f('uq_sessions_api_id'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sessions')
