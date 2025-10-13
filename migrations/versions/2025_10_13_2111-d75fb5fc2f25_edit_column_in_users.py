"""edit column in users

Revision ID: d75fb5fc2f25
Revises: 3beb313cad7c
Create Date: 2025-10-13 21:11:19.998837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd75fb5fc2f25'
down_revision: Union[str, Sequence[str], None] = '3beb313cad7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'tg_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('users', 'user_uuid',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_index(op.f('ix_users_tg_id'), table_name='users')
    op.create_index(op.f('ix_users_tg_id'), 'users', ['tg_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_tg_id'), table_name='users')
    op.create_index(op.f('ix_users_tg_id'), 'users', ['tg_id'], unique=True)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('users', 'user_uuid',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('users', 'tg_id',
               existing_type=sa.BIGINT(),
               nullable=False)
