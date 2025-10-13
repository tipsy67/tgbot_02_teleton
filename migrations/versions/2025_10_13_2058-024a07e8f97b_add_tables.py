"""add tables

Revision ID: 024a07e8f97b
Revises: e9043e558d80
Create Date: 2025-10-13 20:58:04.512896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '024a07e8f97b'
down_revision: Union[str, Sequence[str], None] = 'e9043e558d80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=12), nullable=True),
    sa.Column('language_code', sa.String(length=2), nullable=True),
    sa.Column('user_uuid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_activity', sa.DateTime(), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_tg_id'), 'users', ['tg_id'], unique=True)
    op.create_table('channels',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('prompt', sa.String(), nullable=False),
    sa.Column('system_prompt', sa.String(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_channels_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_channels'))
    )
    op.create_index(op.f('ix_channels_user_id'), 'channels', ['user_id'], unique=False)
    op.add_column('sessions', sa.Column('user_id', sa.BigInteger(), nullable=False))
    op.create_index(op.f('ix_sessions_user_id'), 'sessions', ['user_id'], unique=False)
    op.create_foreign_key(op.f('fk_sessions_user_id_users'), 'sessions', 'users', ['user_id'], ['id'])
    op.drop_column('sessions', 'api_id')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('sessions', sa.Column('api_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('fk_sessions_user_id_users'), 'sessions', type_='foreignkey')
    op.drop_index(op.f('ix_sessions_user_id'), table_name='sessions')
    op.drop_column('sessions', 'user_id')
    op.drop_index(op.f('ix_channels_user_id'), table_name='channels')
    op.drop_table('channels')
    op.drop_index(op.f('ix_users_tg_id'), table_name='users')
    op.drop_table('users')
